"""Attempt 11, family 4b: tail helper, aiming P(eq)*Q(len) at .297-.316 (g .869). Predictor arithmetic: P(eq) .199/.28/.378/.488, Q(len) .6/.785/.85. Test order x how each arm ends x fail form x caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *

SIG = 'static uint8_t *netRecvDone(uint8_t *buf, int got, int size, int *len, uint32_t verbose)\n{\n\t'
SHORT_V = SHORTVV  # void netRecvShort
FAILS = {
 'sret': (SHORTV, 'return netRecvShort(buf, got, size, verbose);'),
 'svoid': (SHORTVV, 'netRecvShort(buf, got, size, verbose);\n\treturn NULL;'),
 'inl': ('', NL + LOG + '\treturn NULL;'),
}
OK = '*len = size;\n\t\t\treturn buf;'


def body(order, fn):
    if order == 'len-eq':
        return 'if (len) {\n\t\tif (got == size) {\n\t\t\t' + OK + '\n\t\t}\n\t}\n\t' + fn
    if order == 'eq-len':
        return 'if (got == size) {\n\t\tif (len) {\n\t\t\t' + OK + '\n\t\t}\n\t}\n\t' + fn
    if order == 'nolen':  # early out on a missing out parameter, then the compare
        return 'if (!len) {\n\t\t' + fn.replace('\n\t', '\n\t\t') + '\n\t}\n\tif (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + fn
    if order == 'ne-nolen':
        f2 = fn.replace('\n\t', '\n\t\t')
        return 'if (got != size) {\n\t\t' + f2 + '\n\t}\n\tif (!len) {\n\t\t' + f2 + '\n\t}\n\t*len = size;\n\treturn buf;'
    if order == 'nolen-ne':
        f2 = fn.replace('\n\t', '\n\t\t')
        return 'if (!len) {\n\t\t' + f2 + '\n\t}\n\tif (got != size) {\n\t\t' + f2 + '\n\t}\n\t*len = size;\n\treturn buf;'
    if order == 'okflag':  # one return at the end of each arm through a local
        return 'if (len && got == size) {\n\t\t*len = size;\n\t} else {\n\t\t' + fn.replace('\n\t', '\n\t\t').replace('return NULL;', 'buf = NULL;').replace('return netRecvShort', 'buf = netRecvShort') + '\n\t}\n\treturn buf;'
    if order == 'eq-var':
        return 'if (got == size) {\n\t\tif (len)\n\t\t\t*len = size;\n\t} else {\n\t\t' + fn.replace('\n\t', '\n\t\t').replace('return NULL;', 'buf = NULL;').replace('return netRecvShort', 'buf = netRecvShort') + '\n\t}\n\treturn buf;'
    raise ValueError(order)


def caller(k):
    call = 'netRecvDone(buf, got, size, len, verbose)'
    d = '\t\tif (size > 0)\n\t\tdo {\n' + BODY + '\t\t} while (got < size);\n'
    z = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
    if k == 'ret':
        return d + '\t\treturn ' + call + ';\n\t}\n' + z
    if k == 'ifnot':
        return d + '\t\tif (' + call + ')\n\t\t\treturn buf;\n\t\treturn NULL;\n\t}\n' + z
    if k == 'ifnot2':
        return d + '\t\tif (!' + call + ')\n\t\t\treturn NULL;\n\t\treturn buf;\n\t}\n' + z
    if k == 'tern':
        return d + '\t\treturn ' + call + ' ? buf : NULL;\n\t}\n' + z
    raise ValueError(k)


def variants():
    for o, fk, ck in itertools.product(('len-eq', 'eq-len', 'nolen', 'ne-nolen', 'nolen-ne', 'okflag', 'eq-var'), FAILS, ('ret', 'ifnot', 'ifnot2', 'tern')):
        helper_, f = FAILS[fk]
        yield '|'.join((o, fk, ck)), helper_ + SIG + NL + body(o, f) + '\n}\n\n' + PRE + caller(ck)
