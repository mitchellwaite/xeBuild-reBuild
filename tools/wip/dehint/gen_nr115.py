"""Attempt 12: gen_nr114 br|ret (select arm `if (!ok) break;`, recv arm `if (!ok) return NULL;`, post-loop `if (!ok) return NULL;`): V=4, C=0.
Left: the unswitched copy's add takes free name got_7 (below size_46), so dom3 swaps the latch compare. Natural spellings that change how many names are free at unswitch."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr114 import build
from nrflip import rep

ADD = 'got += r;\n'
RECVL = 'r = recv(netSock, (char *)buf + got, size - got, 0);\n'
SIZE = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n'
AX = {
    'recv': {
        '': [],
        'left': [(RECVL, 'int left = size - got;\nr = recv(netSock, (char *)buf + got, left, 0);\n')],
        'p': [(RECVL, 'char *p = (char *)buf + got;\nr = recv(netSock, p, size - got, 0);\n')],
        'pl': [(RECVL, 'char *p = (char *)buf + got;\nint left = size - got;\nr = recv(netSock, p, left, 0);\n')],
    },
    'flag': {
        '': [],
        'first': [('log_printf(0, "timeout waiting for data, error %d\\n", WSAGetLastError());\nif (buf != (uint8_t *)&netEmpty)\n free(buf);\nok = 0;',
                   'ok = 0;\nlog_printf(0, "timeout waiting for data, error %d\\n", WSAGetLastError());\nif (buf != (uint8_t *)&netEmpty)\n free(buf);')],
        'eq0': [('if (!ok)', 'if (ok == 0)')],
    },
    'calloc': {
        '': [],
        'void': [('buf = calloc(size, 1);', 'buf = (uint8_t *)calloc(size, 1);')],
        'got0': [('got = 0;\nwhile (got < size) {', 'for (got = 0; got < size;) {')],
    },
    'size': {
        '': [],
        'blk': [('\tuint8_t hdr[4];\n', ''), ('\tr = recv(netSock, (char *)hdr, 4, 0);', '\tuint8_t hdr[4];\n\tr = recv(netSock, (char *)hdr, 4, 0);')],
        'gotdecl': [('int size, got, r;', 'int size, r;\n\tint got;')],
        'order': [('int size, got, r;', 'int r, got, size;')],
    },
}


def variants():
    keys = list(AX)
    for arms in ('br', 'rb'):
        for post in ('ret', 'if'):
            for scope in ('fn', 'pre', 'blk'):
                base = build(arms, post, scope, 0)
                for combo in itertools.product(*[AX[k].items() for k in keys]):
                    s = base
                    ok = True
                    for name, pairs in combo:
                        for a, b in pairs:
                            if a not in s:
                                ok = False
                                break
                            s = s.replace(a, b)
                    if ok:
                        yield '|'.join((arms, post, scope) + tuple(n for n, _ in combo)), s
