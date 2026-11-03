"""Attempt 11, family 4: attempt 8's tail helper with the author's out-parameter guard. In a helper `if (len)` has a reason to be there (it can't see the head's *len = 0), and it folds after IPA inlining. New P(eq) values for the window (g .869: P(eq) .297-.316)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *
from gen_nr73 import caller2

SIG = 'static uint8_t *netRecvDone(uint8_t *buf, int got, int size, int *len, uint32_t verbose)\n{\n\t'
FAIL2 = NL1 + LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree') + '\t\treturn NULL;\n\t'
FAIL1 = NL + LOG + '\treturn NULL;\n}\n\n'
GS = 'if (len)\n\t\t\t*len = size;\n\t\t'
GS1 = 'if (len)\n\t\t*len = size;\n\t'
SH = 'return netRecvShort(buf, got, size, verbose);\n'


def hbody(k):
    b = SIG + NL
    if k == 'eq-g':
        return b + 'if (got == size) {\n\t\t' + GS + 'return buf;\n\t}\n\t' + FAIL1
    if k == 'ne-g':
        return b + 'if (got != size) {\n\t\t' + FAIL2 + '}\n\t' + GS1 + 'return buf;\n}\n\n'
    if k == 'eqand':
        return b + 'if (got == size && len) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + FAIL1
    if k == 'andeq':
        return b + 'if (len && got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + FAIL1
    if k == 'neor':
        return b + 'if (got != size || !len) {\n\t\t' + FAIL2 + '}\n\t*len = size;\n\treturn buf;\n}\n\n'
    if k == 'orne':
        return b + 'if (!len || got != size) {\n\t\t' + FAIL2 + '}\n\t*len = size;\n\treturn buf;\n}\n\n'
    if k == 'nest':  # the len test is separate, its false edge goes to the fail path
        return b + 'if (got == size) {\n\t\tif (len) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t}\n\t' + FAIL1
    if k == 'eqs-g':
        return SHORTV + b + 'if (got == size) {\n\t\t' + GS + 'return buf;\n\t}\n\t' + SH + '}\n\n'
    if k == 'nes-g':
        return SHORTV + b + 'if (got != size)\n\t\t' + SH + '\t' + GS1 + 'return buf;\n}\n\n'
    if k == 'eqs-and':
        return SHORTV + b + 'if (got == size && len) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SH + '}\n\n'
    if k == 'nes-or':
        return SHORTV + b + 'if (got != size || !len)\n\t\t' + SH + '\t*len = size;\n\treturn buf;\n}\n\n'
    if k == 'eqs-nest':
        return SHORTV + b + 'if (got == size) {\n\t\tif (len) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t}\n\t' + SH + '}\n\n'
    if k == 'var-g':
        return b + 'if (got == size) {\n\t\t' + GS + '} else {\n\t\t' + FAIL2.replace('return NULL;', 'buf = NULL;') + '}\n\treturn buf;\n}\n\n'
    if k == 'g-first':  # the store's guard wraps the whole test
        return b + 'if (len) {\n\t\tif (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t}\n\t' + FAIL1
    raise ValueError(k)


KINDS = ('eq-g', 'ne-g', 'eqand', 'andeq', 'neor', 'orne', 'nest', 'eqs-g', 'nes-g', 'eqs-and', 'nes-or', 'eqs-nest', 'var-g', 'g-first')


def variants():
    for hk, ck in itertools.product(KINDS, ('ret', 'var2', 'var3', 'head1', 'ifnot', 'nest')):
        p = PRE
        if ck == 'head1':
            p = p.replace('uint8_t *buf;', 'uint8_t *buf, *ret;')
        yield hk + '|' + ck, hbody(hk) + p + caller2(ck)
