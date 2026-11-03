"""Attempt 2: tails where the short-count test isn't an EQ on two names, so PRED_OPCODE_NONEQUAL doesn't apply."""
import itertools
import gen_nr15 as g

SH = g.SHORT
F = g.FREE
A = g.AFTER
OK = '*len = size;\n\treturn buf;\n'
TAILS = {
    'left-ne': 'left = size - got;\n\t' + A + '\tif (left != 0) {\n\t' + SH.replace('\n\t', '\n\t\t') + F.replace('\n\t', '\n\t\t') + '\n\t}\n\t' + OK,
    'left-if': A + '\tleft = size - got;\n\tif (left) {\n\t' + SH.replace('\n\t', '\n\t\t') + F.replace('\n\t', '\n\t\t') + '\n\t}\n\t' + OK,
    'left-eq': A + '\tleft = size - got;\n\tif (left == 0) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SH + F + '\n',
    'left-not': A + '\tif (!(left = size - got)) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SH + F + '\n',
    'left-loop': A + '\tif (size - got != 0) {\n\t' + SH.replace('\n\t', '\n\t\t') + F.replace('\n\t', '\n\t\t') + '\n\t}\n\t' + OK,
    'gt': A + '\tif (got > size) {\n\t' + SH.replace('\n\t', '\n\t\t') + F.replace('\n\t', '\n\t\t') + '\n\t}\n\t' + OK,
    'le': A + '\tif (got <= size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SH + F + '\n',
    'ne': A + '\tif (got != size) {\n\t' + SH.replace('\n\t', '\n\t\t') + F.replace('\n\t', '\n\t\t') + '\n\t}\n\t' + OK,
}


def variants():
    for s, f, t in itertools.product(g.SEL, g.FORMS, TAILS):
        g.TAILS[t] = TAILS[t]
        v = g.src(s, f, t).replace('int size, got, r, ok;', 'int size, got, r, left;')
        yield '|'.join((s, f, t)), v
