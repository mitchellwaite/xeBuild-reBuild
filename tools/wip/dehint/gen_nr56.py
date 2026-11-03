"""Attempt 7: helper hands back the new total through an out parameter (got stays SSA), status return, log in the caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr52 import *
FAILS = {
 'neg': ('return -1;', 'return 0;', '%s < 0'),
 'negne': ('return -1;', 'return 0;', '%s'),
 'se': ('return SOCKET_ERROR;', 'return 0;', '%s == SOCKET_ERROR'),
 'bool': ('return 0;', 'return 1;', '!%s'),
}
TAILX = TAIL[:TAIL.index('if (verbose)\n\t\t\t\t' + PROG)]


def variants():
    for (a, (fr, okr, test)), nl in itertools.product(FAILS.items(), ('nlh', 'nlc')):
        v = nl == 'nlh'
        fb = ('\t\tif (verbose)\n\t\t\t' + NL + '\n') if v else ''
        h = 'static int netRecvSome(uint8_t *buf, int got, int size, int *total' + (', uint32_t verbose' if v else '') + ')\n{\n\tint r = recv(netSock, (char *)buf + got, size - got, 0);\n\n\tif (r == SOCKET_ERROR) {\n' + fb + '\t\t' + fr + '\n\t}\n\t*total = got + r;\n\t' + okr + '\n}\n\n'
        cnl = '' if v else '\t\t\t\tif (verbose)\n\t\t\t\t\t' + NL + '\n'
        call = 'netRecvSome(buf, got, size, &r' + (', verbose)' if v else ')')
        body = 'if (' + test % call + ') {\n' + cnl + '\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n\t\t\tgot = r;\n'
        yield a + '|' + nl, h + rep(FLIP, (TAILX, body))
