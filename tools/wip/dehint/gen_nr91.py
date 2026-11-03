"""Attempt 10, family 3: size's type and assignment on the flip, with got int. Signed compares come by cast where size is unsigned."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
DECL = 'int size, got, r;'
GET = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {'
LOOP = 'while (got < size) {'
EQ = 'if (got == size) {'
STORE = '*len = size;'
ZERO = ['*len = 0;\n\treturn (uint8_t *)&netEmpty;']

GETS = {
 'plain': GET,
 'cast': 'size = (int)getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {',
 'inline-test': 'if ((size = getBeU32(hdr)) == -1)\n\t\treturn NULL;\n\tif (size) {',
 'inline-both': 'if ((size = getBeU32(hdr)) == -1)\n\t\treturn NULL;\n\tif (size != 0) {',
 'u-temp': '{ uint32_t n = getBeU32(hdr); if (n == 0xffffffff) return NULL; size = n; }\n\tif (size) {',
 'u-temp2': '{ uint32_t n = getBeU32(hdr); size = n; if (n == 0xffffffff) return NULL; }\n\tif (size) {',
 'u-temp3': '{ uint32_t n = getBeU32(hdr); if (n == 0xffffffff) return NULL; if (!n) { *len = 0; return (uint8_t *)&netEmpty; } size = n; }\n\tif (size) {',
 'cmp-ucast': 'size = getBeU32(hdr);\n\tif ((uint32_t)size == 0xffffffff)\n\t\treturn NULL;\n\tif (size) {',
 'cmp-not': 'size = getBeU32(hdr);\n\tif (!~size)\n\t\treturn NULL;\n\tif (size) {',
 'cmp-add': 'size = getBeU32(hdr);\n\tif (size + 1 == 0)\n\t\treturn NULL;\n\tif (size) {',
 'cmp-helper': 'size = getBeU32(hdr);\n\tif (netBadSize(size))\n\t\treturn NULL;\n\tif (size) {',
}
HELPER = 'static int netBadSize(int size)\n{\n\treturn size == -1;\n}\n\n'


def usize(s, loop, sub, eq, calloc, args):
    """size is uint32_t; casts as chosen"""
    s = rep(s, (DECL, 'uint32_t size;\n\tint got, r;'))
    s = rep(s, (LOOP, loop), ('size - got', sub), (EQ, eq))
    if calloc:
        s = rep(s, ('calloc(size, 1)', calloc))
    if args:
        s = rep(s, (', got, size);', ', got, (int)size);'))
    return s


def variants():
    for n, g in GETS.items():
        s = rep(FLIP, (GET, g))
        if n == 'cmp-helper':
            s = HELPER + s
        yield 'int|' + n, s
    # size types that stay signed or same width
    for t in ('long', 'int32_t', 'INT', 'LONG', 'ssize_t', 'off_t', 'SOCKET', 'unsigned', 'uint32_t', 'size_t', 'DWORD', 'u_long'):
        for fn in ('plain', 'cast', 'u-temp'):
            s = rep(FLIP, (GET, GETS[fn]), (DECL, t + ' size;\n\tint got, r;'))
            yield t + '|' + fn + '|nocast', s
    # uint32_t size with signed compares by cast
    L = {'cast': 'while (got < (int)size) {', 'nocast': LOOP, 'ucast': 'while ((uint32_t)got < size) {'}
    S = {'plain': 'size - got', 'cast': '(int)size - got', 'ucast': 'size - (uint32_t)got'}
    E = {'cast': 'if (got == (int)size) {', 'ucast': 'if ((uint32_t)got == size) {', 'plain': EQ}
    for ln, l in L.items():
        for sn, sb in S.items():
            for en, e in E.items():
                for a in (0, 1):
                    for gn in ('plain', 'cmp-ucast'):
                        s = rep(FLIP, (GET, GETS[gn]))
                        yield 'u|%s|%s|%s|%d|%s' % (ln, sn, en, a, gn), usize(s, l, sb, e, None, a)
