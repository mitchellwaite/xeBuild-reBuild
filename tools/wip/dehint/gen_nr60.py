"""Attempt 7: whole loop in a helper that returns a status and hands got back through a pointer, so the status test threads away on every path."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr59 import *
VALS = {'01': ('return 0;', 'return 1;', '!%s'), 'm10': ('return -1;', 'return 0;', '%s < 0'), 'm10ne': ('return -1;', 'return 0;', '%s'), '10': ('return 1;', 'return 0;', '%s')}
TAILS = ('local', 'ptr')


def looph(s, kw, fr, ok, test, tail):
    i = s.index(LOOP_A)
    j = s.index(LOOP_E)
    body = s[i:j]
    body = '\n'.join(l[1:] if l.startswith('\t') else l for l in body.split('\n')).replace('&fds', 'fds').replace('&tv', 'tv')
    body = body.replace('return NULL;', fr)
    h = kw + 'int netRecvBody(uint8_t *buf, int size, uint32_t verbose, fd_set *fds, struct timeval *tv, int *total)\n{\n\tint got, r;\n\n' + body + '\t*total = got;\n\t' + ok + '\n}\n\n'
    s = s[:i] + '\t\tif (' + test % 'netRecvBody(buf, size, verbose, &fds, &tv, &got)' + ')\n\t\t\treturn NULL;\n' + s[j:]
    return h, s


def variants():
    for kw, (a, (fr, ok, t)), rk in itertools.product(('static ', 'static inline '), VALS.items(), ('none', 'eq')):
        s = FLIP
        hdr = ''
        if rk == 'eq':
            hdr += RH['eq'][0]
            s = rep(s, (RECV0, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
        h, s = looph(s, kw, fr, ok, t, 0)
        yield '|'.join((kw.strip(), a, rk)), hdr + h + s
