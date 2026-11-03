"""Attempt 7: netRecvSome updates got through a pointer and returns a status, so the helper's branch survives in its verbose-0 form and the fail edge's share comes from the helper's estimate."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr52 import *
PSIG = 'static int netRecvSome(uint8_t *buf, int *got, int size, uint32_t verbose)\n{\n\tint r = recv(netSock, (char *)buf + *got, size - *got, 0);\n\n'
FAILS = {
 'neg': ('return -1;', 'return 0;', '%s < 0'),
 'negne': ('return -1;', 'return 0;', '%s'),
 'se': ('return SOCKET_ERROR;', 'return 0;', '%s == SOCKET_ERROR'),
 'bool': ('return 0;', 'return 1;', '!%s'),
 'err': ('return 1;', 'return 0;', '%s'),
}
NLS = {'nlh': 1, 'nlc': 0}


def variants():
    for (a, (fr, okr, test)), nl in itertools.product(FAILS.items(), NLS):
        fb = ('\t\tif (verbose)\n\t\t\t' + NL + '\n') if nl == 'nlh' else ''
        h = PSIG + '\tif (r == SOCKET_ERROR) {\n' + fb + '\t\t' + fr + '\n\t}\n\t*got += r;\n\t' + okr + '\n}\n\n'
        cnl = '' if nl == 'nlh' else '\t\t\t\tif (verbose)\n\t\t\t\t\t' + NL + '\n'
        call = 'netRecvSome(buf, &got, size, verbose)'
        body = 'if (' + test % call + ') {\n' + cnl + '\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
        yield a + '|' + nl, h + rep(FLIP, (TAIL[:TAIL.index('if (verbose)\n\t\t\t\t' + PROG)], body))
