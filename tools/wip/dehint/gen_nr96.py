"""Attempt 10, MODEL CHECK: pairs of VRP-folded tests, to land P(stay) in the .84-.86 window. Not a shape to land; checks that the stale lever alone gives the bytes."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
GET = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {\n\t\tbuf = calloc(size, 1);\n'
DECL = 'int size, got, r;'
HEADN = 'n = getBeU32(hdr);\n\tif (n == 0xffffffff)\n\t\treturn NULL;\n\tif (n) {\n\t\tsize = n;\n\t\tbuf = calloc(size, 1);\n'
E = '(uint8_t *)&netEmpty'
ONE = {
 'z-null': 'if (!size) return NULL;\n\t\t',
 'm1-null': 'if (size == -1) return NULL;\n\t\t',
 'm1-free-empty': 'if (size == -1) { free(buf); return ' + E + '; }\n\t\t',
 'z-free-empty': 'if (!size) { free(buf); return ' + E + '; }\n\t\t',
 'z-free-null': 'if (!size) { free(buf); return NULL; }\n\t\t',
 'm1-empty': 'if (size == -1) return ' + E + ';\n\t\t',
 'z-empty': 'if (!size) return ' + E + ';\n\t\t',
}


def variants():
    for a, b in itertools.permutations(ONE, 2):
        yield a + '+' + b, rep(FLIP, (GET, HEADN + '\t\t' + ONE[a] + ONE[b]), (DECL, 'uint32_t n;\n\tint size, got, r;'))
    for a, b in ((x, y) for x in ONE for y in ONE):
        yield a + '/' + b, rep(FLIP, (GET, HEADN + '\t\t' + ONE[a]), ('got = 0;\n', ONE[b] + 'got = 0;\n'), (DECL, 'uint32_t n;\n\tint size, got, r;'))
