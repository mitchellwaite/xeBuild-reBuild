"""Attempt 7: the rest of the task's list. Fail helper, helper for the whole arm or the loop, side select, recv helper's spellings."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr50 import *
NL = "putchar('" + BS + "n');"
LOGV = '\t\tif (verbose)\n\t\t\t' + NL + '\n\t\tlog_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t   WSAGetLastError());\n'
RS = 'static int netRecvSome(char *p, int n, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n'
RH = {
 'none': ('', None),
 'eq': (RS + '\tif (r == SOCKET_ERROR) {\n' + LOGV + '\t\treturn SOCKET_ERROR;\n\t}\n\treturn r;\n}\n\n', 0),
 'early': (RS + '\tif (r != SOCKET_ERROR)\n\t\treturn r;\n' + LOGV.replace('\t\t', '\t', 1).replace('\n\t\t\t' + NL, '\n\t\t' + NL).replace('\t\tlog_printf', '\tlog_printf').replace('\t\t\t   WSA', '\t\t   WSA') + '\treturn SOCKET_ERROR;\n}\n\n', 0),
 'free': (None, 1),
}
FH = 'static uint8_t *netRecvFail(uint8_t *buf)\n{\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;\n}\n\n'
LSEL2 = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {\n\t\t\t\tlog_printf(0, "timeout waiting for data, error %d' + BS + 'n", WSAGetLastError());\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
ARM_A = '\tif (size) {\n\t\tbuf = calloc(size, 1);'
ARM_E = '\t\treturn NULL;\n\t}\n\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n'


def arm(s):
    """the `if (size)` arm as static netRecvBody"""
    i = s.index(ARM_A) + len('\tif (size) {\n')
    j = s.index(ARM_E) + len('\t\treturn NULL;\n')
    body = s[i:j]
    body = '\n'.join(l[1:] if l.startswith('\t') else l for l in body.split('\n'))
    body = body.replace('&fds', 'fds').replace('&tv', 'tv')
    h = 'static uint8_t *netRecvBody(int *len, int size, uint32_t verbose, fd_set *fds, struct timeval *tv)\n{\n\tuint8_t *buf;\n\tint got, r;\n\n' + body + '}\n\n'
    s = s[:i] + '\t\treturn netRecvBody(len, size, verbose, &fds, &tv);\n' + s[j:]
    s = s.replace('\tuint8_t *buf;\n\tint size, got, r;', '\tint size, r;')
    return h, s


def variants():
    for sel, rk, fh, bd in itertools.product(('plain', 'side'), ('none', 'eq', 'early'), ('none', 'fail'), ('none', 'arm')):
        s = FLIP
        hdr = ''
        if sel == 'side':
            s = rep(s, (LSEL, LSEL2))
        rh, _ = RH[rk]
        if rk != 'none':
            hdr += rh
            s = rep(s, (RECV0, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
        if fh == 'fail':
            hdr += FH
            s = s.replace(FREE3, 'return netRecvFail(buf);')
            s = s.replace('if (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\treturn NULL;', 'return netRecvFail(buf);')
        if bd == 'arm':
            h, s = arm(s) if 'return NULL;\n\t}\n\t*len = 0' in s else (None, s)
            if h is None:
                continue
            hdr += h
        yield '|'.join((sel, rk, fh, bd)), hdr + s
