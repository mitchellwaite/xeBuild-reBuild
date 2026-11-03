"""Attempt 12: tidying gen_nr119 v0 (text 0 data 0). Spellings of the select arm's test, ok's scope and init, loop form, what the select arm assigns; all checked with nrobjbest."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, SEL, RECV
from gen_nr117 import CALLOC, NL, LOGT, STORE

SELT = {'ge': 'got >= size', 'eq': 'got == size', 'le': 'size <= got', 'nlt': '!(got < size)'}
SCOPE = {
    'fn': ('int ok = 1;\n', '', ''),
    'decl': ('int ok;\n', 'ok = 1;\n', ''),
    'list': ('', '', ''),
    'if': ('', 'int ok = 1;\n', ''),
    'got': ('', '', 'ok'),
}
LOOPT = ('ok != 1', '!ok', 'ok == 0')
LOOP = ('while', 'for')
SELEXIT = {'ret': 'return NULL;', 'block': '{\nreturn NULL;\n}'}


def build(st, sc, lt, loop, sx):
    decl, pre, extra = SCOPE[sc]
    inner = (SEL + LOGS + FREE + 'size = got;\n}\nif (' + SELT[st] + ')\n' + SELEXIT[sx] + '\n' + RECV + NLOGR + FREE + 'ok = 0;\n}\nif (' + lt + ')\nbreak;\n' + 'got += r;\n' + PRINT)
    h = HEAD
    if sc == 'list':
        h = h.replace('int size, got, r;', 'int size, got, r, ok = 1;')
    elif sc == 'got':
        h = h.replace('int size, got, r;', 'int size, got, r, ok;')
        pre = 'ok = 1;\n'
    elif decl:
        h = h.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl)
    lp = ('got = 0;\nwhile (got < size) {\n' if loop == 'while' else 'for (got = 0; got < size;) {\n') + inner + '}\n'
    tail = 'if (ok != 1)\n return NULL;\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n'
    return h + pre + CALLOC + lp + tail + '}\n' + FOOT


def variants():
    for st in SELT:
        for sc in SCOPE:
            for lt in LOOPT:
                for loop in LOOP:
                    for sx in SELEXIT:
                        yield '|'.join((st, sc, lt.replace(' ', ''), loop, sx)), build(st, sc, lt, loop, sx)
