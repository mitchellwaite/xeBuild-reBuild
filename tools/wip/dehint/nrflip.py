"""Attempt 5 base: netRecvVerbose as in src/net.c minus the asm (same as drafts/net_netRecvVerbose_flip.c), for generators to edit with text replacements."""
import os
d = os.path.dirname(os.path.abspath(__file__))
_t = open(os.path.join(d, '..', '..', '..', 'src', 'net.c')).read()
FLIP = _t[_t.index('uint8_t *netRecvVerbose(int *len, uint32_t verbose)'):_t.index('#define netRecv(len)')]
FLIP = FLIP.replace('\t\t__asm__ ("" : : "g"(got));\n', '')
ADD = 'got += r;'
LEN = 'size - got'
ARG = '(char *)buf + got'
RECV = 'r = recv(netSock, (char *)buf + got, size - got, 0);'
LOGA = 'log_printf(0, "received only %x of %x bytes! fail\\n", got, size);'
SEL = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {'
GOT0 = 'got = 0;'


def rep(s, *pairs):
    for a, b in pairs:
        assert a in s, a
        s = s.replace(a, b)
    return s
