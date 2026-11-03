"""Attempt 8: tail in a static helper sized above early-inline growth, so the short-count path is a call at profile_estimate (call heuristic on the guard or on got == size) and stays out of line until IPA. Axes: loop form, helper scope, helper return."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
a = FLIP.index('\t\twhile (got < size)')
b = FLIP.index('\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)')
c = FLIP.index('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;')
PRE, LOOP, TAILX, ZERO = FLIP[:a], FLIP[a:b], FLIP[b:c], FLIP[c:]
BODY = LOOP[LOOP.index('{\n') + 2:LOOP.rindex('\t\t}')]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');\n\t"
LOG = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n'
NL2 = NL.replace('\t\t', '\t\t\t').replace("n');\n\t", "n');\n\t\t")


def looptext(k):
    if k == 'while':
        return LOOP
    if k == 'do>':
        return '\t\tif (size > 0) do {\n' + BODY + '\t\t} while (got < size);\n'
    if k == 'do>b':
        return '\t\tif (size > 0) {\n\t\t\tdo {\n' + BODY + '\t\t\t} while (got < size);\n\t\t}\n'


def variants():
    for lk, hk in itertools.product(('while', 'do>'), ('short', 'shortnl', 'tail', 'tailok', 'tail0', 'shortret', 'shortretnl')):
        L = looptext(lk)
        if hk == 'short':    # log and free in a helper, newlines in the caller
            h = 'static void netRecvShort(uint8_t *buf, int got, int size)\n{\n\t' + LOG + '}\n\n'
            t = '\t\t' + NL2 + 'if (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\t' + NL2 + 'netRecvShort(buf, got, size);\n\t\treturn NULL;\n\t}\n'
        elif hk == 'shortnl':
            h = 'static void netRecvShort(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + LOG + '}\n\n'
            t = '\t\t' + NL2 + 'if (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\tnetRecvShort(buf, got, size, verbose);\n\t\treturn NULL;\n\t}\n'
        elif hk == 'shortret':
            h = 'static uint8_t *netRecvShort(uint8_t *buf, int got, int size)\n{\n\t' + LOG + '\treturn NULL;\n}\n\n'
            t = '\t\t' + NL2 + 'if (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\t' + NL2 + 'return netRecvShort(buf, got, size);\n\t}\n'
        elif hk == 'shortretnl':
            h = 'static uint8_t *netRecvShort(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + LOG + '\treturn NULL;\n}\n\n'
            t = '\t\t' + NL2 + 'if (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\treturn netRecvShort(buf, got, size, verbose);\n\t}\n'
        elif hk == 'tail':   # whole tail
            h = 'static uint8_t *netRecvDone(uint8_t *buf, int got, int size, int *len, uint32_t verbose)\n{\n\t' + NL + 'if (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + NL + LOG + '\treturn NULL;\n}\n\n'
            t = '\t\treturn netRecvDone(buf, got, size, len, verbose);\n\t}\n'
        elif hk == 'tailok':  # status return, caller stores
            h = 'static int netRecvDone(uint8_t *buf, int got, int size, uint32_t verbose)\n{\n\t' + NL + 'if (got == size)\n\t\treturn 1;\n\t' + NL + LOG + '\treturn 0;\n}\n\n'
            t = '\t\tif (!netRecvDone(buf, got, size, verbose))\n\t\t\treturn NULL;\n\t\t*len = size;\n\t\treturn buf;\n\t}\n'
        elif hk == 'tail0':  # helper from got == size
            h = 'static uint8_t *netRecvDone(uint8_t *buf, int got, int size, int *len, uint32_t verbose)\n{\n\tif (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + NL + LOG + '\treturn NULL;\n}\n\n'
            t = '\t\t' + NL2 + 'return netRecvDone(buf, got, size, len, verbose);\n\t}\n'
        yield lk + '|' + hk, h + PRE + L + t + ZERO
