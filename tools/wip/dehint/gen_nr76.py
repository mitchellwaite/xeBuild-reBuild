"""Attempt 8: status-returning tail helper: the store stays in the caller, so store's stale freq is set by the caller's test and log's by the helper's. Axes: helper's J layout, caller's test, first newline in or out of the helper."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *
SV = 'static void netRecvShort(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + LOG + '}\n\n'
LOG2 = LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree')


def h(kind, fn):
    sig = 'static int netRecvDone(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + (NL if fn else '')
    if kind == 'eq':
        return sig + 'if (got == size)\n\t\treturn 1;\n\t' + NL + LOG + '\treturn 0;\n}\n\n'
    if kind == 'ne':
        return sig + 'if (got != size) {\n\t\t' + NL1 + LOG2 + '\t\treturn 0;\n\t}\n\treturn 1;\n}\n\n'
    if kind == 'eqs':
        return SV + sig + 'if (got == size)\n\t\treturn 1;\n\tnetRecvShort(buf, got, size, verbose);\n\treturn 0;\n}\n\n'
    if kind == 'nes':
        return SV + sig + 'if (got != size) {\n\t\tnetRecvShort(buf, got, size, verbose);\n\t\treturn 0;\n\t}\n\treturn 1;\n}\n\n'


def variants():
    d = '\t\tif (size > 0)\n\t\tdo {\n' + BODY + '\t\t} while (got < size);\n'
    z = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
    S = '*len = size;\n\t\t\treturn buf;\n\t\t'
    call = 'netRecvDone(buf, got, size, verbose)'
    tests = {
        'if': 'if (' + call + ') {\n\t\t\t' + S + '}\n\t\treturn NULL;\n\t}\n',
        'ifeq1': 'if (' + call + ' == 1) {\n\t\t\t' + S + '}\n\t\treturn NULL;\n\t}\n',
        'not': 'if (!' + call + ')\n\t\t\treturn NULL;\n\t\t*len = size;\n\t\treturn buf;\n\t}\n',
        'ne1': 'if (' + call + ' != 1)\n\t\t\treturn NULL;\n\t\t*len = size;\n\t\treturn buf;\n\t}\n',
        'buf0': 'if (' + call + ')\n\t\t\t*len = size;\n\t\telse\n\t\t\tbuf = NULL;\n\t\treturn buf;\n\t}\n',
    }
    for ik, tk, fn in itertools.product(('eq', 'ne', 'eqs', 'nes'), tests, (True, False)):
        pn = '' if fn else '\t\t' + NL1
        yield '|'.join((ik, tk, 'nlin' if fn else 'nlout')), h(ik, fn) + PRE + d + pn + tests[tk] + z
