"""Attempt 11, family 1: the author's `if (outLen) *outLen = len;` idiom on len's later stores. Outer shape x success store x zero arm's store x tail. No asm."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
i = FLIP.index('\tif (size) {\n')
HEAD = FLIP[:i]
j = FLIP.index('\t\tif (verbose)\n\t\t\tputchar(\'\\n\');\n\t\tif (got == size) {')
BODY = FLIP[i + len('\tif (size) {\n'):j]
E = '(uint8_t *)&netEmpty'
FREE = 'if (buf != ' + E + ')\n\t\t\tfree(buf);\n\t\t'
LOG = 'if (verbose)\n\t\t\tputchar(\'\\n\');\n\t\tlog_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n\t\t' + FREE + 'return NULL;\n'
NL = 'if (verbose)\n\t\t\tputchar(\'\\n\');\n\t\t'
STORE = {
 'plain': '*len = size;',
 'g': 'if (len)\n\t\t\t\t*len = size;',
 'gn': 'if (len != NULL)\n\t\t\t\t*len = size;',
 'ggot': 'if (len)\n\t\t\t\t*len = got;',
}
ZERO = {
 'plain': '*len = 0;',
 'g': 'if (len)\n\t\t\t*len = 0;',
 'gn': 'if (len != NULL)\n\t\t\t*len = 0;',
 'gsize': 'if (len)\n\t\t\t*len = size;',
}


def tail(t, st):
    if t == 'eq':
        return NL + 'if (got == size) {\n\t\t\t' + st + '\n\t\t\treturn buf;\n\t\t}\n\t\t' + LOG
    if t == 'eqand':  # the store's guard joins the compare: the false edge goes to the log
        return NL + 'if (got == size && len) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\t' + LOG
    if t == 'andeq':
        return NL + 'if (len && got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\t' + LOG
    if t == 'ne':
        return NL + 'if (got != size) {\n\t\t\t' + LOG.replace('\n\t\t', '\n\t\t\t').rstrip('\t') + '\t\t}\n\t\t' + st + '\n\t\treturn buf;\n'
    if t == 'nl1':  # first newline inside each branch
        return 'if (got == size) {\n\t\t\t' + NL.replace('\n\t\t', '\n\t\t\t') + st + '\n\t\t\treturn buf;\n\t\t}\n\t\t' + NL + LOG
    raise ValueError(t)


def mk(sh, t, st, z):
    b = BODY + '\t\t' + tail(t, STORE[st]) if True else ''
    ze = '\t\t' + ZERO[z] + '\n\t\treturn ' + E + ';\n'
    if sh == 'flip':
        return HEAD + '\tif (size) {\n' + b + '\t}\n' + ze.replace('\t\t', '\t').replace('\n\t*len', '\n\t\t*len') + '}\n'
    if sh == 'else':
        return HEAD + '\tif (size) {\n' + b + '\t} else {\n' + ze + '\t}\n}\n'
    if sh == 'old':  # zero first, early return; body at one level deeper is harmless
        return HEAD + '\tif (size == 0) {\n' + ze + '\t}\n\t{\n' + b + '\t}\n}\n'
    if sh == 'not':
        return HEAD + '\tif (!size) {\n' + ze + '\t} else {\n' + b + '\t}\n}\n'
    raise ValueError(sh)


def variants():
    for sh in ('flip', 'else', 'old', 'not'):
        for t in ('eq', 'ne', 'nl1', 'eqand', 'andeq'):
            for st in STORE:
                if t in ('eqand', 'andeq') and st != 'plain':
                    continue
                for z in ZERO:
                    yield '|'.join((sh, t, st, z)), mk(sh, t, st, z)
