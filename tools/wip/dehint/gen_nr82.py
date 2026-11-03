"""Attempt 9: scalars in nested scopes (r per use, got/buf in if (size), size at its getBeU32, r in the loop body), x flip/old head x select x hdr block. Expected no-ops: scalars have no clobbers."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
HSEL = 'r = select(0, &fds, NULL, NULL, &tv);\n\tif ('
HRCV = 'r = recv(netSock, (char *)hdr, 4, 0);'


def make(rs, gs, bs, ss, hd, head, sel):
    s = FLIP
    dec = 'int size, got, r;\n'
    keep = ['size'] if not ss else []
    if not gs:
        keep.append('got')
    if not rs:
        keep.append('r')
    if rs:
        s = rep(s, (HSEL, 'int r = select(0, &fds, NULL, NULL, &tv);\n\tif ('))
        s = rep(s, (HRCV, 'r = recv(netSock, (char *)hdr, 4, 0);'))
        s = rep(s, (SEL, '{\n\t\t\tint r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {'))
        s = rep(s, (ADD, 'got += r;\n\t\t\t}'))
    s = rep(s, (dec, ('int ' + ', '.join(keep) + ';\n') if keep else ''))
    if gs:
        s = rep(s, (GOT0, 'int got = 0;'))
    if bs:
        s = rep(s, ('\tuint8_t *buf;\n', ''), ('buf = calloc', 'uint8_t *buf = calloc'))
    if ss:
        s = rep(s, ('size = getBeU32(hdr);', 'int size = getBeU32(hdr);'))
    if hd:
        s = rep(s, ('\tuint8_t hdr[4];\n', ''), (HRCV, 'uint8_t hdr[4];\n\t' + HRCV))
    if sel == 'side':
        if rs:
            s = rep(s, ('int r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {', 'int r;\n\t\t\tif ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'))
        else:
            s = rep(s, (SEL, 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'))
    return s


def variants():
    for k in itertools.product((0, 1), (0, 1), (0, 1), (0, 1), (0, 1), ('flip',), ('plain', 'side')):
        yield 'r%d g%d b%d s%d h%d %s %s' % k, make(*k)
