"""Attempt 10, family 2: netRecvVerbose's own declaration on the flip: len, return and verbose types. Callers are left alone (netRecvVerbose isn't in net.h)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
SIG = 'uint8_t *netRecvVerbose(int *len, uint32_t verbose)'
LENS = {'int': 'int *len', 'u32': 'uint32_t *len', 'uint': 'unsigned int *len', 'long': 'long *len', 'ulong': 'unsigned long *len',
        'size_t': 'size_t *len', 'void': 'void *len', 'char': 'char *len'}
RETS = {'u8': 'uint8_t *', 'void': 'void *', 'char': 'char *', 'uchar': 'unsigned char *', 'int': 'int *', 'u32': 'uint32_t *'}
VERBS = {'u32': 'uint32_t verbose', 'uint': 'unsigned int verbose', 'ulong': 'unsigned long verbose', 'size_t': 'size_t verbose',
         'DWORD': 'DWORD verbose', 'int': 'int verbose', 'BOOL': 'BOOL verbose', 'long': 'long verbose', 'u8': 'uint8_t verbose', 'char': 'char verbose',
         'schar': 'signed char verbose', 'u16': 'uint16_t verbose', 'short': 'short verbose', 'bool': '_Bool verbose'}


def mk(l, r, v):
    s = FLIP.replace(SIG, RETS[r] + 'netRecvVerbose(' + LENS[l] + ', ' + VERBS[v] + ')')
    if l == 'void':
        s = s.replace('*len =', '*(int *)len =')
    if l == 'char':
        s = s.replace('*len =', '*(int *)len =')
    return s


def variants():
    for l in LENS:
        for r in RETS:
            for v in VERBS:
                # one axis at a time, plus len x return with verbose u32
                if (l != 'int') + (r != 'u8') + (v != 'u32') <= 1 or v == 'u32':
                    yield '|'.join((l, r, v)), mk(l, r, v)
