"""Attempt 7: helper returns a status, recv's count comes back through an out parameter, so got keeps its PHI (no nested loop from the two latches), log in the caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr52 import *
PSIG = 'static int netRecvSome(uint8_t *buf, int got, int size, int *r, uint32_t verbose)\n{\n\t*r = recv(netSock, (char *)buf + got, size - got, 0);\n\n'
PSIGN = 'static int netRecvSome(uint8_t *buf, int got, int size, int *r)\n{\n\t*r = recv(netSock, (char *)buf + got, size - got, 0);\n\n'
LSIG = 'static int netRecvSome(uint8_t *buf, int got, int size, int *r%s)\n{\n\tint n = recv(netSock, (char *)buf + got, size - got, 0);\n\n'
FAILS = {
 'neg': ('return -1;', 'return 0;', '%s < 0'),
 'negne': ('return -1;', 'return 0;', '%s'),
 'se': ('return SOCKET_ERROR;', 'return 0;', '%s == SOCKET_ERROR'),
 'bool': ('return 0;', 'return 1;', '!%s'),
}
TAILX = TAIL[:TAIL.index('got += r;')]


def variants():
    for (a, (fr, okr, test)), nl, loc in itertools.product(FAILS.items(), ('nlh', 'nlc'), ('star', 'local')):
        v = nl == 'nlh'
        fb = ('\t\tif (verbose)\n\t\t\t' + NL + '\n') if v else ''
        if loc == 'star':
            h = (PSIG if v else PSIGN) + '\tif (*r == SOCKET_ERROR) {\n' + fb + '\t\t' + fr + '\n\t}\n\t' + okr + '\n}\n\n'
        else:
            h = LSIG % (', uint32_t verbose' if v else '') + '\tif (n == SOCKET_ERROR) {\n' + fb + '\t\t' + fr + '\n\t}\n\t*r = n;\n\t' + okr + '\n}\n\n'
        cnl = '' if v else '\t\t\t\tif (verbose)\n\t\t\t\t\t' + NL + '\n'
        call = 'netRecvSome(buf, got, size, &r' + (', verbose)' if v else ')')
        body = 'if (' + test % call + ') {\n' + cnl + '\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
        yield a + '|' + nl + '|' + loc, h + rep(FLIP, (TAILX, body))
