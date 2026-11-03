"""Attempt 12: three exits, no bottom test (fncmp's match with the bottom test loses BB27's .p2align: 2.25% exit, 61 < freq_max/100).
Each arm's exit is return or break, post-loop forms, flag scope and flag per arm."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, SEL, RECV

CALLOC = 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n'
NL = 'if (verbose)\n putchar(\'\\n\');\n'
LOGT = 'log_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n'
STORE = '*len = size;\nreturn buf;\n'
POSTS = {
    'ret': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n',
    'if': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + '}\nreturn NULL;\n',
    'ne': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got != size) {\n' + NL + LOGT + FREE + 'return NULL;\n}\n' + STORE,
    'ifne': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got != size) {\n' + NL + LOGT + FREE + 'return NULL;\n}\n' + STORE + '}\nreturn NULL;\n',
    'ifelse': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n}\nreturn NULL;\n',
    'failbuf': lambda t, nt: 'if (' + t + ') {\nreturn NULL;\n}\n' + NL + 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + NL + LOGT + FREE + 'return NULL;\n',
}
SCOPES = {
    'fn': ('int ok = 1;', '', ''),
    'pre': ('int ok;', 'ok = 1;\n', ''),
    'blk': ('', 'int ok = 1;\n', ''),
    'bodyset': ('int ok;', 'ok = 1;\n', 'ok = 1;\n'),
}
ARMS = ('br', 'bb', 'rb')  # select arm, recv arm: b = break, r = return; rr has no post test


def build(arms, post, scope, split, order=0):
    decl, pre, body = SCOPES[scope]
    ex = lambda c: 'if (!ok)\n ' + ('break;' if c == 'b' else 'return NULL;') + '\n'
    inner = body + SEL + LOGS + FREE + 'ok = 0;\n}\n' + ex(arms[0]) + RECV + NLOGR + FREE + 'ok = 0;\n}\n' + ex(arms[1]) + 'got += r;\n' + PRINT
    if split:  # the return arm's test on a body-scoped flag of its own
        rarm = 0 if arms[0] == 'r' else 1
        inner = (SEL + LOGS + FREE + ('bad = 1;' if rarm == 0 else 'ok = 0;') + '\n}\n' +
                 ('if (bad)\n return NULL;\n' if rarm == 0 else ex('b')) + RECV + NLOGR + FREE + ('bad = 1;' if rarm == 1 else 'ok = 0;') + '\n}\n' +
                 ('if (bad)\n return NULL;\n' if rarm == 1 else ex('b')) + 'got += r;\n' + PRINT)
        inner = 'int bad = 0;\n' + inner
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    return h + CALLOC + pre + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + POSTS[post]('!ok', 'ok') + '}\n' + FOOT


def variants():
    for arms in ARMS:
        for post in POSTS:
            for scope in SCOPES:
                yield '|'.join((arms, post, scope)), build(arms, post, scope, 0)
                if arms != 'bb':
                    yield '|'.join((arms, post, scope, 'split')), build(arms, post, scope, 1)
