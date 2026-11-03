"""Attempt 11, family 2: len tests that exit, in places someone might write them: joined to the size test (`if (size && len)`), to the -1 test, `if (!size || !len)`. Zero arm x success store guards."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
OUTER = '\tif (size) {\n'
ZEROTAIL = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n'
GZ = '\tif (len)\n\t\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n'
Z2 = '\tif (!len)\n\t\treturn NULL;\n\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n'
Z3 = '\tif (len) {\n\t\t*len = 0;\n\t\treturn (uint8_t *)&netEmpty;\n\t}\n\treturn NULL;\n'
OUTERS = {
 's&&l': 'if (size && len) {', 'l&&s': 'if (len && size) {', 's&&ln': 'if (size != 0 && len != NULL) {',
 'ln&&s': 'if (len != NULL && size != 0) {', 'n1': 'if (size != -1 && size && len) {',
}
MINUS = {
 'p': 'if (size == -1)\n\t\treturn NULL;',
 'm|l': 'if (size == -1 || !len)\n\t\treturn NULL;',
 'l|m': 'if (!len || size == -1)\n\t\treturn NULL;',
 'l;m': 'if (!len)\n\t\treturn NULL;\n\tif (size == -1)\n\t\treturn NULL;',
 'm;l': 'if (size == -1)\n\t\treturn NULL;\n\tif (!len)\n\t\treturn NULL;',
}
ZS = {'p': ZEROTAIL, 'g': GZ, 'ifnot': Z2, 'ifelse': Z3}
ST = {'p': '*len = size;', 'g': 'if (len)\n\t\t\t\t*len = size;'}
CAL = 'buf = calloc(size, 1);\n'
LATE = {
 'p': '',
 'arm': '\t\tif (!len) {\n\t\t\tnetFree(buf);\n\t\t\treturn NULL;\n\t\t}\n',  # attempt 10's candidate, as the control
}


def mk(o, m, z, st, l):
    s = FLIP
    if o != 'p':
        s = rep(s, (OUTER, '\t' + OUTERS[o] + '\n'))
    s = rep(s, (MINUS['p'], MINUS[m]), (ZEROTAIL, ZS[z]), ('*len = size;', ST[st]))
    if l != 'p':
        s = rep(s, (CAL, CAL + LATE[l]))
    return s


def variants():
    for o in ['p'] + list(OUTERS):
        for m in MINUS:
            for z in ZS:
                for st in ST:
                    if o == 'p' and m == 'p' and z == 'p' and st == 'p':
                        yield 'control-arm', mk(o, m, z, st, 'arm')
                    yield '|'.join((o, m, z, st)), mk(o, m, z, st, 'p')
