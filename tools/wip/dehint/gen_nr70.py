"""Attempt 8: why buf != &netEmpty exists: the size test only wraps the transfer, and the tail (got == size, store, log) is shared with the zero path, which threads away."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
i = FLIP.index('\tif (size) {')
HEAD = FLIP[:i]
a = FLIP.index('\t\twhile (got < size)')
b = FLIP.index('\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)')
LOOP = FLIP[a:b]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');"
WAIT = 'if (verbose)\n\t\t\tprintf("waiting for 0x%x bytes' + BS + 'n", size);'
LOG = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'


def tail(k, st):
    if k == 'eq':
        return 'if (got == size) {\n\t\t*len = %s;\n\t\treturn buf;\n\t}\n\t' % st + NL + '\n\t' + LOG + '\n}\n\n'
    if k == 'ne':
        return 'if (got != size) {\n\t' + NL + '\n\t' + LOG + '\n\t}\n\t*len = %s;\n\treturn buf;\n}\n\n' % st


def variants():
    for hk, nk, tk, st, lk in itertools.product(('dflt', 'dfltbuf', 'else', 'elsezero', 'ter'), ('in', 'and'), ('eq', 'ne'), ('size', 'got'), ('while', 'guard')):
        loop = LOOP if lk == 'while' else '\t\tif (size > 0)\n' + LOOP
        nl = '\t\t' + NL + '\n' if nk == 'in' else ''
        nlo = '' if nk == 'in' else '\tif (size && verbose)\n\t\tputchar(\'' + BS + 'n\');\n\t'
        xf = 'buf = calloc(size, 1);\n\t\t' + WAIT + '\n' + loop + nl
        if hk == 'dflt':
            h = '\tgot = 0;\n\tbuf = (uint8_t *)&netEmpty;\n\tif (size) {\n\t\t' + xf + '\t}\n'
        elif hk == 'dfltbuf':
            h = '\tbuf = (uint8_t *)&netEmpty;\n\tif (size) {\n\t\t' + xf.replace('buf = calloc(size, 1);', 'buf = calloc(size, 1);') + '\t}\n'
            h = '\tgot = 0;\n' + h
        elif hk == 'else':
            h = '\tgot = 0;\n\tif (size)\n\t{\n\t\t' + xf + '\t} else\n\t\tbuf = (uint8_t *)&netEmpty;\n'
        elif hk == 'elsezero':
            h = '\tgot = 0;\n\tif (size == 0)\n\t\tbuf = (uint8_t *)&netEmpty;\n\telse {\n\t\t' + xf + '\t}\n'
        else:
            h = '\tgot = 0;\n\tbuf = size ? calloc(size, 1) : (uint8_t *)&netEmpty;\n\tif (size) {\n\t\t' + WAIT + '\n' + loop + nl + '\t}\n'
        s = HEAD + h + '\t' + nlo + tail(tk, st)
        s = s.replace('\t\tgot = 0;\n', '')
        yield '|'.join((hk, nk, tk, st, lk)), s
