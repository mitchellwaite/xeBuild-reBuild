"""Attempt 7: netRecvSome with the verbose newline inside and the log in the caller, so the fail edge's share comes from the helper's estimate while R's block keeps the caller's frequency."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
NL = "putchar('" + BS + "n');"
LOGR = 'log_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t\t\t   WSAGetLastError());\n'
FREE3 = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;'
RECV0 = ('r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\tif (verbose)\n\t\t\t\t\t' + NL + '\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n')
SIG = 'static int netRecvSome(char *p, int n, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n'
H = {
 'ret': SIG + '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t\treturn SOCKET_ERROR;\n\t}\n\treturn r;\n}\n\n',
 'retm1': SIG + '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t\treturn -1;\n\t}\n\treturn r;\n}\n\n',
 'nest': SIG + '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t}\n\treturn r;\n}\n\n',
 'and': SIG + '\tif (r == SOCKET_ERROR && verbose)\n\t\t' + NL + '\n\treturn r;\n}\n\n',
 'zero': SIG + '\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\t' + NL + '\n\t\treturn -1;\n\t}\n\tif (verbose)\n\t\tprintf("");\n\treturn r;\n}\n\n',
}
TEST = {'eq': 'r == SOCKET_ERROR', 'lt': 'r < 0'}


def variants():
    for (a, h), (b, t) in itertools.product(H.items(), TEST.items()):
        if a == 'zero':
            continue
        yield a + '|' + b, h + rep(FLIP, (RECV0, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (' + t + ') {\n\t\t\t\t' + LOGR + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
