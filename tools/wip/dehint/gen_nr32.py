"""Attempt 5, angles 1, 3, 4: log block forms, loop-exit forms, size/got typing at the recv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
L = 'received only %x of %x bytes! fail' + BS + 'n'
LOGS = {
 'plain': LOGA,
 'scoped': '{ int n = got; log_printf(0, "' + L + '", n, size); }',
 'scopedu': '{ uint32_t n = got; log_printf(0, "' + L + '", n, size); }',
 'scopedu2': '{ uint32_t n = got, m = size; log_printf(0, "' + L + '", n, m); }',
 'castu': 'log_printf(0, "' + L + '", (uint32_t)got, size);',
 'castuu': 'log_printf(0, "' + L + '", (uint32_t)got, (uint32_t)size);',
 'castl': 'log_printf(0, "' + L + '", (long)got, size);',
 'castul': 'log_printf(0, "' + L + '", (unsigned long)got, (unsigned long)size);',
 'castcast': 'log_printf(0, "' + L + '", (int)(uint32_t)got, size);',
 'fmt': '{ const char *fmt = "' + L + '"; log_printf(0, fmt, got, size); }',
 'ncarry': '{ int n = got; if (verbose) putchar(10); log_printf(0, "' + L + '", n, size); }',
}
SELS = {
 'plain': SEL,
 'notfirst': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (!r || r == SOCKET_ERROR) {',
 'zero-first': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == 0 || r == SOCKET_ERROR) {',
 'le': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r <= 0) {',
}
ADDS = {
 'plain': ADD,
 'sum': 'got = got + r;',
 'rsum': 'got = r + got;',
 'uadd': 'got += (uint32_t)r;',
 'uadd2': 'got = (uint32_t)got + (uint32_t)r;',
 'ptr': 'got = (char *)buf + got + r - (char *)buf;',
}
RECVS = {
 'plain': RECV,
 'left': '{ int left = size - got; r = recv(netSock, (char *)buf + got, left, 0); }',
 'leftu': '{ uint32_t left = size - got; r = recv(netSock, (char *)buf + got, left, 0); }',
 'left2': '{ uint32_t left = size; left -= got; r = recv(netSock, (char *)buf + got, left, 0); }',
 'ptr': '{ char *p = (char *)buf + got; r = recv(netSock, p, size - got, 0); }',
 'idx': 'r = recv(netSock, (char *)&buf[got], size - got, 0);',
 'off': '{ uint32_t off = got; r = recv(netSock, (char *)buf + off, size - off, 0); }',
 'offs': '{ uint32_t off = got, left = size - off; r = recv(netSock, (char *)buf + off, left, 0); }',
}


def variants():
    P = 'plain'
    for ln, l in LOGS.items():
        for rn, r in RECVS.items():
            yield '|'.join((ln, P, P, rn)), rep(FLIP, (LOGA, l), (RECV, r))
    for an, a in ADDS.items():
        for rn, r in RECVS.items():
            yield '|'.join((P, P, an, rn)), rep(FLIP, (ADD, a), (RECV, r))
    for an, a in ADDS.items():
        for sn, se in SELS.items():
            yield '|'.join((P, sn, an, P)), rep(FLIP, (ADD, a), (SEL, se))
