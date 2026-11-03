"""Attempt 7: the loop helper with the status test spelled so X's edge to J is the unlikely one (`status == 0 && got == size` puts .28 on it) and the log block gets the rest of X's flow."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr60 import *
NLC = "if (verbose)\n\t\t\tputchar('" + BS + "n');\n"
LOG = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);'
TAIL_A = "\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\tif (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n"
VALS = {'m10': ('return -1;', 'return 0;'), '01': ('return 0;', 'return 1;'), 'se': ('return SOCKET_ERROR;', 'return 0;')}
OKT = {'m10': ['status == 0', '!status'], 'se': ['status == 0', 'status != SOCKET_ERROR'], '01': ['status == 1', 'status']}
BADT = {'m10': ['status != 0', 'status < 0', 'status'], 'se': ['status == SOCKET_ERROR', 'status'], '01': ['status != 1', '!status']}
NLW = ('helper', 'caller')


def make(a, fr, ok, okt, badt, nlw, kw, shape):
    s = FLIP
    i = s.index(LOOP_A)
    j = s.index(LOOP_E)
    body = s[i:j]
    body = '\n'.join(l[1:] if l.startswith('\t') else l for l in body.split('\n')).replace('&fds', 'fds').replace('&tv', 'tv')
    body = body.replace('return NULL;', fr)
    nlh = "\tif (verbose)\n\t\tputchar('" + BS + "n');\n" if nlw == 'helper' else ''
    h = kw + 'int netRecvBody(uint8_t *buf, int size, uint32_t verbose, fd_set *fds, struct timeval *tv, int *total)\n{\n\tint got, r;\n\n' + body + nlh + '\t*total = got;\n\t' + ok + '\n}\n\n'
    call = '\t\tstatus = netRecvBody(buf, size, verbose, &fds, &tv, &got);\n'
    nlc = "\t\tif (" + okt + ' && verbose)\n\t\t\tputchar(\'' + BS + "n');\n" if nlw == 'caller' else ''
    k = s.index(TAIL_A)
    if shape == 'early':
        tail = call + nlc + '\t\tif (' + okt + ' && got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\tif (' + badt + ')\n\t\t\treturn NULL;\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + "n');\n"
        s = s[:i] + tail + s[k + len(TAIL_A):]
    else:  # nest: whole rest under the ok test
        tail = call + nlc + '\t\tif (' + okt + ' && got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\tif (' + okt + ') {\n\t\t\tif (verbose)\n\t\t\t\tputchar(\'' + BS + "n');\n\t\t\t" + LOG + '\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t}\n\t\treturn NULL;\n\t}\n'
        l = s.index('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;')
        s = s[:i] + tail + s[l:]
    s = s.replace('int size, got, r;', 'int size, got, r, status;')
    return h + s


def variants():
    for a, (fr, ok) in VALS.items():
        for okt, badt, nlw, kw, shape in itertools.product(OKT[a], BADT[a], NLW, ('static ',), ('early', 'nest')):
            if shape == 'nest' and badt != BADT[a][0]:
                continue
            yield '|'.join((a, okt, badt, nlw, shape)), make(a, fr, ok, okt, badt, nlw, kw, shape)
