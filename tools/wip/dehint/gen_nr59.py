"""Attempt 7: whole arm or whole loop in a helper, static or static inline, with or without the recv helper."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr58 import *
LOOP_A = '\t\tgot = 0;\n\t\twhile (got < size) {'
LOOP_E = "\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\tif (got == size) {"


def loop(s, kw, neg):
    i = s.index(LOOP_A)
    j = s.index(LOOP_E)
    body = s[i:j]
    body = '\n'.join(l[1:] if l.startswith('\t') else l for l in body.split('\n')).replace('&fds', 'fds').replace('&tv', 'tv')
    body = body.replace('return NULL;', 'return -1;')
    h = kw + 'int netRecvBody(uint8_t *buf, int size, uint32_t verbose, fd_set *fds, struct timeval *tv)\n{\n\tint got, r;\n\n' + body + '\treturn got;\n}\n\n'
    s = s[:i] + '\t\tgot = netRecvBody(buf, size, verbose, &fds, &tv);\n\t\tif (got < 0)\n\t\t\treturn NULL;\n' + s[j:]
    return h, s


def variants():
    for kw, shape, rk in itertools.product(('static ', 'static inline '), ('arm', 'loop'), ('none', 'eq')):
        s = FLIP
        hdr = ''
        if rk == 'eq':
            hdr += RH['eq'][0]
            s = rep(s, (RECV0, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
        if shape == 'arm':
            h, s = arm(s)
            h = h.replace('static ', kw, 1)
        else:
            h, s = loop(s, kw, 1)
        yield '|'.join((kw.strip(), shape, rk)), hdr + h + s
