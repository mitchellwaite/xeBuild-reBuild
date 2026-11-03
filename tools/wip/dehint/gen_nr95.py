"""Attempt 10, MODEL CHECK: predictor sweep of the VRP-folded test (n unsigned, size its int copy): test x exit arm x position. Window wanted: P(stay) about .84-.86."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
GET = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {\n\t\tbuf = calloc(size, 1);\n'
DECL = 'int size, got, r;'
HEADN = 'n = getBeU32(hdr);\n\tif (n == 0xffffffff)\n\t\treturn NULL;\n\tif (n) {\n\t\tsize = n;\n\t\tbuf = calloc(size, 1);\n'
VERB = 'if (verbose)\n\t\t\tprintf("waiting for 0x%x bytes\\n", size);\n'
G0 = 'got = 0;\n'
E = '(uint8_t *)&netEmpty'
TESTS = {'z': '!size', 'm1': 'size == -1', 'zc': 'size == 0'}
ARMS = {
 'null': 'return NULL;',
 'buf': 'return buf;',
 'empty': 'return ' + E + ';',
 'len0-empty': '*len = 0; return ' + E + ';',
 'len0-buf': '*len = 0; return buf;',
 'lensz-buf': '*len = size; return buf;',
 'free-null': 'free(buf); return NULL;',
 'free-empty': 'free(buf); return ' + E + ';',
 'free-len0': 'free(buf); *len = 0; return ' + E + ';',
 'neq-free': 'if (buf != ' + E + ') free(buf); return NULL;',
 'log-null': 'log_printf(0, "received only %x of %x bytes! fail\\n", size, size); return NULL;',
 'log-free': 'log_printf(0, "received only %x of %x bytes! fail\\n", size, size); free(buf); return NULL;',
 'one': 'return (uint8_t *)1;',
 'buf2': 'return buf + 1;',
 'hdr': 'return (uint8_t *)len;',
}
ELSE = ('', 'else')


def variants():
    for tn, t in TESTS.items():
        for an, a in ARMS.items():
            arm = 'if (' + t + ') { ' + a + ' }\n\t\t'
            yield '%s|%s|calloc' % (tn, an), rep(FLIP, (GET, HEADN + '\t\t' + arm), (DECL, 'uint32_t n;\n\tint size, got, r;'))
            yield '%s|%s|preloop' % (tn, an), rep(FLIP, (GET, HEADN), (G0, arm + G0), (DECL, 'uint32_t n;\n\tint size, got, r;'))
