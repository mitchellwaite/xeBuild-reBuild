"""Attempt 7: netRecvSome computes its own recv arguments, newline in the helper, log and progress in the caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr52 import *
BODY = {
 'args': SIG + FAILV + '\treturn r;\n}\n\n',
 'args-nest': SIG + '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t}\n\treturn r;\n}\n\n',
 'args-and': SIG + '\tif (r == SOCKET_ERROR && verbose)\n\t\t' + NL + '\n\treturn r;\n}\n\n',
}
TAIL2 = TAIL[:TAIL.index('got += r;')]


def variants():
    for a, h in BODY.items():
        for t in ('r == SOCKET_ERROR', 'r < 0'):
            body = 'r = netRecvSome(buf, got, size, verbose);\n\t\t\tif (' + t + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
            yield a + '|' + t, h + rep(FLIP, (TAIL2, body))
