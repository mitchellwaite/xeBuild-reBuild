"""Attempt 7: netRecvSome big enough not to be early-inlined (holds the progress output), newline in the helper or not, log in the caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
NL = "putchar('" + BS + "n');"
LOGR = 'log_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t\t\t   WSAGetLastError());\n'
FREE3 = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;'
PROG = 'printf("received 0x%08x of 0x%08x' + BS + 'r", got, size);'
TAIL = ('r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\tif (verbose)\n\t\t\t\t\t' + NL + '\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n\t\t\tgot += r;\n\t\t\tif (verbose)\n\t\t\t\t' + PROG + '\n')
SIG = 'static int netRecvSome(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\tint r = recv(netSock, (char *)buf + got, size - got, 0);\n\n'
FAILV = '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t\treturn SOCKET_ERROR;\n\t}\n'
H = {
 # returns r, adds locally for the message
 'r-loc': SIG + FAILV + '\tif (verbose)\n\t\tprintf("received 0x%08x of 0x%08x' + BS + 'r", got + r, size);\n\treturn r;\n}\n\n',
 'r-add': SIG + FAILV + '\tgot += r;\n\tif (verbose)\n\t\t' + PROG + '\n\treturn r;\n}\n\n',
 # returns the new total
 'tot': SIG + FAILV + '\tgot += r;\n\tif (verbose)\n\t\t' + PROG + '\n\treturn got;\n}\n\n',
}
LOGC = {'clog': lambda t: 'if (' + t + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'}


def variants():
    for a, h in H.items():
        for t in ('r == SOCKET_ERROR', 'r < 0'):
            if a == 'tot':
                t2 = t.replace('r ', 'got ')
                body = 'got = netRecvSome(buf, got, size, verbose);\n\t\t\tif (' + t2 + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
                yield a + '|' + t, h + rep(FLIP, (TAIL, body))
                body = 'r = netRecvSome(buf, got, size, verbose);\n\t\t\tif (' + t + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n\t\t\tgot = r;\n'
                yield a + '|r|' + t, h + rep(FLIP, (TAIL, body))
            else:
                body = 'r = netRecvSome(buf, got, size, verbose);\n\t\t\tif (' + t + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n\t\t\tgot += r;\n'
                yield a + '|' + t, h + rep(FLIP, (TAIL, body))
