"""Attempt 10: a zero test that exists twice at profile_estimate and is threaded or folded after it, raising the block before the loop (stale, gen_nr91's u-temp3 margin +801).
Head shapes: buf chosen by a first test on size, then the zero arm on a second test."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
GET = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {\n\t\tbuf = calloc(size, 1);\n'
TAIL = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}'
GETSZ = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n'
E = '(uint8_t *)&netEmpty'
NT = 'uint32_t n = getBeU32(hdr);\n\tif (n == 0xffffffff)\n\t\treturn NULL;\n'
HEADS = {
 'flip': (GET, TAIL),
 # second test, buf picked by the first
 'tern-if': (GETSZ + '\tbuf = size ? calloc(size, 1) : ' + E + ';\n\tif (size) {\n', TAIL),
 'tern-ret': (GETSZ + '\tbuf = size ? calloc(size, 1) : ' + E + ';\n\tif (size) {\n', '\t*len = 0;\n\treturn buf;\n}'),
 'if-if': (GETSZ + '\tif (size)\n\t\tbuf = calloc(size, 1);\n\telse\n\t\tbuf = ' + E + ';\n\tif (size) {\n', '\t*len = 0;\n\treturn buf;\n}'),
 'if-if-size': (GETSZ + '\tif (size)\n\t\tbuf = calloc(size, 1);\n\telse\n\t\tbuf = ' + E + ';\n\tif (size) {\n', '\t*len = size;\n\treturn buf;\n}'),
 'def-if': (GETSZ + '\tbuf = ' + E + ';\n\tif (size)\n\t\tbuf = calloc(size, 1);\n\tif (size) {\n', '\t*len = 0;\n\treturn buf;\n}'),
 'def-if0': (GETSZ + '\tbuf = ' + E + ';\n\tif (size != 0)\n\t\tbuf = calloc(size, 1);\n\tif (size != 0) {\n', '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}'),
 'tern-ne': (GETSZ + '\tbuf = size == 0 ? ' + E + ' : calloc(size, 1);\n\tif (size != 0) {\n', '\t*len = 0;\n\treturn buf;\n}'),
 'buf-test': (GETSZ + '\tbuf = size ? calloc(size, 1) : ' + E + ';\n\tif (buf != ' + E + ') {\n', '\t*len = 0;\n\treturn buf;\n}'),
 'buf-test2': (GETSZ + '\tbuf = size ? calloc(size, 1) : ' + E + ';\n\tif (buf != ' + E + ') {\n', TAIL),
 # temp of another type, inner test on the converted name
 'n-nest': ('{\n\t' + NT + '\tif (n) {\n\t\tsize = n;\n\t\tif (size) {\n\t\tbuf = calloc(size, 1);\n', None),
 'n-size-nest': ('{\n\t' + NT + '\tsize = n;\n\tif (n) {\n\t\tif (size) {\n\t\tbuf = calloc(size, 1);\n', None),
 'n-and': ('{\n\t' + NT + '\tsize = n;\n\tif (n && size) {\n\t\tbuf = calloc(size, 1);\n', None),
}


def variants():
    for hn, (h, t) in HEADS.items():
        s = FLIP
        if t is None:
            s = rep(s, (GET, h), (TAIL, '\t}\n' * (1 if hn == 'n-and' else 2) + TAIL))
        else:
            s = rep(s, (GET, h), (TAIL, t))
        yield hn, s
