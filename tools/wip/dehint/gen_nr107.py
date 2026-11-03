"""Attempt 11, leftovers: tests of fds/tv after the calloc (expected real); a loop condition on r that VRP folds (dead exit, lands in J); the helper's `!len` with a constant-return arm (const_return predictor, for log 280-281)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
import gen_nr105 as g
CAL = 'buf = calloc(size, 1);\n'
NF = '{ netFree(buf); return NULL; }\n'
TESTS = {
 'tv': 'if (!tv.tv_sec) ' + NF, 'tv1': 'if (tv.tv_sec != 15) ' + NF, 'fd': 'if (!fds.fd_count) ' + NF,
 'isset': 'if (!FD_ISSET(netSock, &fds)) ' + NF, 'hdr': 'if (!hdr) ' + NF, 'pfd': 'if (!&fds) ' + NF,
}
W = 'while (got < size) {'
LOOPS = {
 'rand': 'while (got < size && r != SOCKET_ERROR) {', 'randr': 'while (r != SOCKET_ERROR && got < size) {',
 'for': 'for (; got < size && r != SOCKET_ERROR; ) {',
 'r0': 'while (got < size && r != 0 && r != SOCKET_ERROR) {',
}
E = '(uint8_t *)&netEmpty'
ARMS = {
 'const': 'return ' + E + ';',
 'free-const': g.FREE + 'return ' + E + ';',
 'vput-const': g.NL1 + 'return ' + E + ';',
 'log-const': g.L2 + 'return ' + E + ';',
}


def variants():
    for k, t in TESTS.items():
        yield 'test|' + k, rep(FLIP, (CAL, CAL + '\t\t' + t))
    for k, l in LOOPS.items():
        yield 'loop|' + k, rep(FLIP, (W, l))
    for an, a in ARMS.items():
        g.ARMS[an] = a
        for tl in g.TAILS:
            yield '|'.join(('arm', an, tl)), g.mk(an, 'not', 'afternl', tl, 'ifnot2')
