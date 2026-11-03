"""Attempt 8: recv in a helper with a status and an out parameter for r (PHI<-1,0> isn't folded by phiopt; r's pointer leaves got alone), so the log stays in the caller and the threaded fail edge is the only thing moving R. x loop/tail forms."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *
RECV0 = ('r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\tif (verbose)\n\t\t\t\t\tputchar(\'' + BS + 'n\');\n\t\t\t\tlog_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t\t\t   WSAGetLastError());\n\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;\n\t\t\t}\n')
LOGR = 'log_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t\t\t   WSAGetLastError());\n\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;\n\t\t\t}\n'
H = {
    'neg0': ('static int netRecvSome(char *p, int n, int *got, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\treturn -1;\n\t}\n\t*got = r;\n\treturn 0;\n}\n\n',
             'if (netRecvSome((char *)buf + got, size - got, &r, verbose) < 0) {\n\t\t\t\t' + LOGR),
    'eq': ('static int netRecvSome(char *p, int n, int *got, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\treturn SOCKET_ERROR;\n\t}\n\t*got = r;\n\treturn 0;\n}\n\n',
           'if (netRecvSome((char *)buf + got, size - got, &r, verbose) == SOCKET_ERROR) {\n\t\t\t\t' + LOGR),
    '12': ('static int netRecvSome(char *p, int n, int *got, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n\tif (r == SOCKET_ERROR) {\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\treturn 0;\n\t}\n\t*got = r;\n\treturn 1;\n}\n\n',
           'if (!netRecvSome((char *)buf + got, size - got, &r, verbose)) {\n\t\t\t\t' + LOGR),
}


def variants():
    for rk, tk in itertools.product(H, ('flip', 'ne|ret', 'ne|ifnot', 'eq|ifnot', 'eqs|ret')):
        hh, rc = H[rk]
        if tk == 'flip':
            yield rk + '|flip', hh + rep(FLIP, (RECV0, rc))
            continue
        hk, ck = tk.split('|')
        d = '\t\tif (size > 0)\n\t\tdo {\n' + rep(BODY, (RECV0.replace('\n\t\t\t', '\n\t\t\t'), rc)) + '\t\t} while (got < size);\n'
        call = 'netRecvDone(buf, got, size, len, verbose)'
        t = ('return ' + call + ';\n\t}\n') if ck == 'ret' else ('if (' + call + ')\n\t\t\treturn buf;\n\t\treturn NULL;\n\t}\n')
        yield rk + '|' + tk, hh + helper(hk, True) + PRE + d + t + '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
