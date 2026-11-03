"""Attempt 7: loop helper, status spellings, with and without the recv helper; nest shape, ok flag kept in a variable, several tail orders."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr61 import *
NLB = "\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n"
FREEL = '\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n'
LOG2 = '\t\t' + LOG + '\n'
STORE = '\t\t\t*len = size;\n\t\t\treturn buf;\n'
TEN = lambda t: t.replace('\n\t', '\n\t\t').replace('\t\t\t\t\t', '\t\t\t\t')
SH = {
 # J first, then a test for the error return
 'a': lambda ok, bad, call: call + '\t\tif (%s && got == size) {\n%s\t\t}\n\t\tif (%s)\n\t\t\treturn NULL;\n' % (ok, STORE, bad) + NLB + LOG2 + FREEL + '\t\treturn NULL;\n\t}\n',
 # log guarded by the ok test
 'b': lambda ok, bad, call: call + '\t\tif (%s && got == size) {\n%s\t\t}\n\t\tif (%s) {\n\t\t\tif (verbose)\n\t\t\t\tputchar(\'%sn\');\n\t\t\t%s\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t}\n\t\treturn NULL;\n\t}\n' % (ok, STORE, ok, BS, LOG),
 # nested ok
 'c': lambda ok, bad, call: call + '\t\tif (%s) {\n\t\t\tif (got == size) {\n\t%s\t\t\t}\n\t\t\tif (verbose)\n\t\t\t\tputchar(\'%sn\');\n\t\t\t%s\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t}\n\t\treturn NULL;\n\t}\n' % (ok, STORE.replace('\t\t\t', '\t\t\t\t').replace('\t\t\t\t\t', '\t\t\t\t'), BS, LOG),
 # short count first
 'd': lambda ok, bad, call: call + '\t\tif (%s)\n\t\t\treturn NULL;\n\t\tif (got != size) {\n\t\t\tif (verbose)\n\t\t\t\tputchar(\'%sn\');\n\t\t\t%s\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t\treturn NULL;\n\t\t}\n\t\t*len = size;\n\t\treturn buf;\n\t}\n' % (bad, BS, LOG),
 'e': lambda ok, bad, call: call + '\t\tif (%s && got != size) {\n\t\t\tif (verbose)\n\t\t\t\tputchar(\'%sn\');\n\t\t\t%s\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t\treturn NULL;\n\t\t}\n\t\tif (%s)\n\t\t\treturn NULL;\n\t\t*len = size;\n\t\treturn buf;\n\t}\n' % (ok, BS, LOG, bad),
}
VALS2 = {'m10': ('return -1;', 'return 0;', ['status == 0', '!status'], ['status != 0', 'status < 0']), '01': ('return 0;', 'return 1;', ['status == 1', 'status', 'status != 0'], ['status != 1', '!status', 'status == 0'])}


def make2(a, fr, ok, okt, badt, shape, rk):
    s = FLIP
    hdr = ''
    if rk == 'eq':
        hdr = RH['eq'][0]
        s = rep(s, (RECV0, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
    i = s.index(LOOP_A)
    j = s.index(LOOP_E)
    body = '\n'.join(l[1:] if l.startswith('\t') else l for l in s[i:j].split('\n')).replace('&fds', 'fds').replace('&tv', 'tv').replace('return NULL;', fr)
    h = 'static int netRecvBody(uint8_t *buf, int size, uint32_t verbose, fd_set *fds, struct timeval *tv, int *total)\n{\n\tint got, r;\n\n' + body + "\tif (verbose)\n\t\tputchar('" + BS + "n');\n\t*total = got;\n\t" + ok + '\n}\n\n'
    l = s.index('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;')
    s = s[:i] + SH[shape](okt, badt, '\t\tstatus = netRecvBody(buf, size, verbose, &fds, &tv, &got);\n') + s[l:]
    return hdr + h + s.replace('int size, got, r;', 'int size, got, r, status;')


def variants():
    for a, (fr, ok, oks, bads) in VALS2.items():
        for okt, badt, shape, rk in itertools.product(oks, bads, SH, ('none', 'eq')):
            yield '|'.join((a, okt, badt, shape, rk)), make2(a, fr, ok, okt, badt, shape, rk)
