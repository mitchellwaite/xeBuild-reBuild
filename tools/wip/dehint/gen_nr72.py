"""Attempt 8: do form with a pointer-returning tail helper. Target (from gen_nr71 v9): guard .85-.89 (opcode positive + call, no early return), P(eq) .44-.51 in the helper (opcode + call on the fail block, no early return): log <= R, store under the head failures, margin > 0."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
a = FLIP.index('\t\twhile (got < size)')
c = FLIP.index('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;')
b = FLIP.index('\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)')
PRE, LOOP, ZERO = FLIP[:a], FLIP[a:b], FLIP[c:]
BODY = LOOP[LOOP.index('{\n') + 2:LOOP.rindex('\t\t}')]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');\n\t"
NL1 = "if (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\t"
LOG = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n'
SHORTV = 'static uint8_t *netRecvShort(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + LOG + '\treturn NULL;\n}\n\n'
SHORTVV = 'static void netRecvShort(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + LOG + '}\n\n'


def helper(kind, firstnl):
    fn = NL if firstnl else ''
    sig = 'static uint8_t *netRecvDone(uint8_t *buf, int got, int size, int *len, uint32_t verbose)\n{\n\t'
    if kind == 'eq':
        return sig + fn + 'if (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + NL + LOG + '\treturn NULL;\n}\n\n'
    if kind == 'ne':
        return sig + fn + 'if (got != size) {\n\t\t' + NL1 + LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree') + '\t\treturn NULL;\n\t}\n\t*len = size;\n\treturn buf;\n}\n\n'
    if kind == 'eqs':
        return SHORTV + sig + fn + 'if (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\treturn netRecvShort(buf, got, size, verbose);\n}\n\n'
    if kind == 'nes':
        return SHORTV + sig + fn + 'if (got != size)\n\t\treturn netRecvShort(buf, got, size, verbose);\n\t*len = size;\n\treturn buf;\n}\n\n'
    if kind == 'nesv':
        return SHORTVV + sig + fn + 'if (got != size) {\n\t\tnetRecvShort(buf, got, size, verbose);\n\t\treturn NULL;\n\t}\n\t*len = size;\n\treturn buf;\n}\n\n'
    if kind == 'var':  # one return
        return sig + fn + 'if (got == size)\n\t\t*len = size;\n\telse {\n\t\t' + NL1 + LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree') + '\t\tbuf = NULL;\n\t}\n\treturn buf;\n}\n\n'
    if kind == 'vars':
        return SHORTVV + sig + fn + 'if (got == size)\n\t\t*len = size;\n\telse {\n\t\tnetRecvShort(buf, got, size, verbose);\n\t\tbuf = NULL;\n\t}\n\treturn buf;\n}\n\n'


def caller(kind, nl):
    call = 'netRecvDone(buf, got, size, len, verbose)'
    d = '\t\tdo {\n' + BODY + '\t\t} while (got < size);\n'
    pn = '\t\t' + NL1 if nl else ''
    if kind == 'ret':
        return '\t\tif (size > 0)\n' + d + pn + 'return ' + call + ';\n\t}\n' + ZERO
    if kind == 'var':
        return '\t\tif (size > 0)\n' + d + pn + 'buf = ' + call + ';\n\t\treturn buf;\n\t}\n' + ZERO
    if kind == 'late':	# one return at the end of the function
        return '\t\tif (size > 0)\n' + d + pn + 'buf = ' + call + ';\n\t} else {\n\t*len = 0;\n\tbuf = (uint8_t *)&netEmpty;\n\t}\n\treturn buf;\n}\n\n'
    if kind == 'gotoz':
        return '\t\tif (size <= 0)\n\t\t\tgoto done;\n' + d + 'done:\n' + pn + 'return ' + call + ';\n\t}\n' + ZERO
    if kind == 'while':
        return LOOP + pn + 'return ' + call + ';\n\t}\n' + ZERO


def variants():
    for hk, ck, nlk in itertools.product(('eq', 'ne', 'eqs', 'nes', 'nesv', 'var', 'vars'), ('ret', 'var', 'late', 'gotoz', 'while'), (True, False)):
        yield '|'.join((hk, ck, 'nlin' if nlk else 'nlout')), helper(hk, nlk) + PRE + caller(ck, not nlk) + ''
