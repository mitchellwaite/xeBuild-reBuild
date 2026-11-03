"""Attempt 12: gen_nr116 size|ok|rb: V=0, C=0 in fncmp, but the store block is 104 in the clone, over freq_max/100 (97), so it gets a .p2align the reference lacks.
Post-loop forms that lower J or P(eq). Check V=C=0 rows with nrobjbest.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, SEL, RECV

CALLOC = 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n'
NL = 'if (verbose)\n putchar(\'\\n\');\n'
LOGT = 'log_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n'
STORE = '*len = size;\nreturn buf;\n'
SELA = {
    'size': ('size = got;', 'got >= size', 'return NULL;'),
    'size=': ('size = got;', 'got == size', 'return NULL;'),
    'sizele': ('size = got;', 'size <= got', 'return NULL;'),
}
FLAGS = {'ok': ('int ok = 1;\n', 'ok = 0;', '!ok', 'ok'), 'failed': ('int failed = 0;\n', 'failed = 1;', 'failed', '!failed'),
         'blk': ('', 'ok = 0;', '!ok', 'ok')}
POSTS = {
    'ret': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n',
    'if': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + '}\nreturn NULL;\n',
    'ne': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got != size) {\n' + NL + LOGT + FREE + 'return NULL;\n}\n' + STORE,
    'ifne': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got != size) {\n' + NL + LOGT + FREE + 'return NULL;\n}\n' + STORE + '}\nreturn NULL;\n',
    'and': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got != size) {\n' + NL + LOGT + FREE + 'buf = NULL;\n} else\n*len = size;\nreturn buf;\n',
    'andeq': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got == size)\n*len = size;\nelse {\n' + NL + LOGT + FREE + 'buf = NULL;\n}\nreturn buf;\n',
    'flagtail': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n}\nreturn NULL;\n',
    'verb': lambda t, nt: 'if (' + nt + ' && verbose)\n putchar(\'\\n\');\nif (' + nt + ' && got == size) {\n' + STORE + '}\nif (' + t + ')\n return NULL;\n' + NL + LOGT + FREE + 'return NULL;\n',
    'status': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + '}\nbuf = NULL;\nreturn buf;\n',
}


def build(sa, fl, post):
    a_s, t_s, x_s = SELA[sa]
    decl, a_r, t_r, nt = FLAGS[fl]
    inner = SEL + LOGS + FREE + a_s + '\n}\nif (' + t_s + ')\n' + x_s + '\n' + RECV + NLOGR + FREE + a_r + '\n}\nif (' + t_r + ')\nbreak;\n' + 'got += r;\n' + PRINT
    pre = 'int ok = 1;\n' if fl == 'blk' else ''
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    return h + pre + CALLOC + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + POSTS[post](t_r, nt) + '}\n' + FOOT


def variants():
    for sa in SELA:
        for fl in FLAGS:
            for post in POSTS:
                yield '|'.join((sa, fl, post)), build(sa, fl, post)
