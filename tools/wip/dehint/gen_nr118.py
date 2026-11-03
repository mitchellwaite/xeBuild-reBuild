"""Attempt 12: gen_nr117 with the recv failure's work split between the arm in the loop and the post-loop test, so the post-loop test isn't a bare null return.
Target: stale J 400..487 (at .199 store <= 97, the clone's freq_max/100). Now 523 = .9 * (291 + 282)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, SEL, RECV
from gen_nr117 import CALLOC, NL, LOGT, STORE

RLOG = {'log': NLOGR}
ARMS = {
    # name: arm body in the loop (after the recv test), post-loop body before return
    'arm-free': (NLOGR + FREE, ''),
    'post-free': (NLOGR, FREE),
    'post-all': ('', NLOGR + FREE),
    'post-log': (NL, 'log_printf(0, "could not receive data on socket, error %d\\n", WSAGetLastError());\n' + FREE),
}
TAILS = {
    'ret': lambda t, nt, b: 'if (' + t + ') {\n' + b + 'return NULL;\n}\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n',
    'else': lambda t, nt, b: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n}\n' + b + 'return NULL;\n',
}
FLAGS = {
    'ok': ('int ok = 1;\n', 'ok = 0;', '!ok', 'ok', '!ok'),
    'r': ('', '', 'r == SOCKET_ERROR', 'r != SOCKET_ERROR', 'r == SOCKET_ERROR'),
    'r-': ('', '', 'r == -1', 'r != -1', 'r == SOCKET_ERROR'),
    'okset': ('int ok = 1;\n', 'ok = r != SOCKET_ERROR;', '!ok', 'ok', None),
}
SELS = {
    'size': ('size = got;', 'got >= size', 'return NULL;'),
    'ok': ('ok = 0;', '!ok', 'return NULL;'),
    'ret': (None, None, None),
}


def build(sel, arm, tail, fl):
    decl, a_r, t, nt, xt = FLAGS[fl]
    body, b = ARMS[arm]
    sa, st, sx = SELS[sel]
    if sel == 'ok':
        decl = 'int ok = 1;\n'
    if sa:
        s = SEL + LOGS + FREE + sa + '\n}\nif (' + st + ')\n' + sx + '\n'
    else:
        s = SEL + LOGS + FREE + 'return NULL;\n}\n'
    if fl == 'okset':
        r = 'r = recv(netSock, (char *)buf + got, size - got, 0);\nok = r != SOCKET_ERROR;\nif (!ok) {\n' + body + '}\nif (!ok)\nbreak;\n'
    elif arm == 'post-all' and fl.startswith('r'):
        r = 'r = recv(netSock, (char *)buf + got, size - got, 0);\nif (' + xt + ')\nbreak;\n'
    else:
        r = RECV + body + a_r + '\n}\nif (' + xt + ')\nbreak;\n' if xt else ''
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    inner = s + r + 'got += r;\n' + PRINT
    return h + CALLOC + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + TAILS[tail](t, nt, b) + '}\n' + FOOT


def variants():
    for sel in SELS:
        for arm in ARMS:
            for tail in TAILS:
                for fl in FLAGS:
                    yield '|'.join((sel, arm, tail, fl)), build(sel, arm, tail, fl)
