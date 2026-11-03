"""Attempt 6: reuse of one C variable. Roles of head select (hs), head recv (hr), loop select (ls), loop recv (lr):
which local holds each result; plus got initialised at the declaration or at function start, and declaration order/scope."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
HS = 'r = select(0, &fds, NULL, NULL, &tv);\n\tif (r == SOCKET_ERROR || r == 0) {\n\t\tlog_printf(0, "timeout waiting for data, %d'
HR = 'r = recv(netSock, (char *)hdr, 4, 0);\n\tif (r == SOCKET_ERROR || r == 0) {'
LS = SEL
LR = 'r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\t\tif (r == SOCKET_ERROR) {'
DECL = 'int size, got, r;'
A = 'got += r;'


def build(hs, hr, ls, lr, decl=None, extra=()):
    s = FLIP
    s = rep(s, (HS, HS.replace('r =', hs + ' =', 1).replace('(r ==', '(' + hs + ' ==').replace('|| r ==', '|| ' + hs + ' ==')))
    s = rep(s, (HR, HR.replace('r =', hr + ' =', 1).replace('(r ==', '(' + hr + ' ==').replace('|| r ==', '|| ' + hr + ' ==')))
    s = rep(s, (LS, LS.replace('r =', ls + ' =', 1).replace('(r ==', '(' + ls + ' ==').replace('|| r ==', '|| ' + ls + ' ==')))
    s = rep(s, (LR, LR.replace('r =', lr + ' =', 1).replace('(r ==', '(' + lr + ' ==')))
    s = rep(s, (A, 'got += ' + lr + ';'))
    used = []
    for v in (hs, hr, ls, lr):
        if v not in ('size', 'got') and v not in used:
            used.append(v)
    s = rep(s, (DECL, decl or 'int ' + ', '.join(['size', 'got'] + used) + ';'))
    for a, b in extra:
        s = rep(s, (a, b))
    return s


def variants():
    for hs, hr in itertools.product(('r', 'got', 'size', 'n'), repeat=2):
        for ls, lr in (('r', 'r'), ('n', 'r'), ('r', 'n'), ('m', 'r'), ('r', 'm'), ('m', 'k')):
            yield '|'.join((hs, hr, ls, lr)), build(hs, hr, ls, lr)
            yield '|'.join((hs, hr, ls, lr, 'revdecl')), build(hs, hr, ls, lr, None, ()).replace('int size, got', 'int got, size')
            # got initialised at start and again before the loop
            if hs != 'got' and hr != 'got':
                yield '|'.join((hs, hr, ls, lr, 'got0')), build(hs, hr, ls, lr).replace('int size, got', 'int size, got = 0')
                yield '|'.join((hs, hr, ls, lr, 'got0only')), build(hs, hr, ls, lr).replace('int size, got', 'int size, got = 0').replace('\t\tgot = 0;\n', '')
