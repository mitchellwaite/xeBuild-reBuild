"""Attempt 11, family 3: no zero arm in the source. buf is &netEmpty or calloc's, one flow runs through the loop and the one store, and the zero path is threaded out later (that would explain buf != &netEmpty at the frees, and tests that are gone by the output).
Allocation x how the zero path skips the verbose output x tail x store."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
i = FLIP.index('\tif (size) {\n')
HEAD = FLIP[:i]
a = FLIP.index('\t\t\tr = select(0, &fds, NULL, NULL, &tv);')
b = FLIP.index('\t\tif (verbose)\n\t\t\tputchar(\'\\n\');\n\t\tif (got == size) {')
LOOP = FLIP[a:b].replace('\n\t', '\n').replace('\t\t\tr = select', '\t\tr = select', 1).rstrip() + '\n'
assert LOOP.rstrip().endswith('}')
E = '(uint8_t *)&netEmpty'
ALLOC = {
 'tern': '\tbuf = size ? calloc(size, 1) : ' + E + ';\n',
 'ifelse': '\tif (size)\n\t\tbuf = calloc(size, 1);\n\telse\n\t\tbuf = ' + E + ';\n',
 'def': '\tbuf = ' + E + ';\n\tif (size)\n\t\tbuf = calloc(size, 1);\n',
 'not': '\tif (!size)\n\t\tbuf = ' + E + ';\n\telse\n\t\tbuf = calloc(size, 1);\n',
}
W = 'printf("waiting for 0x%x bytes\\n", size);\n'
NLC = "putchar('\\n');\n"
GUARD = {'vs': 'verbose && size', 'sv': 'size && verbose', 'bufne': 'verbose && buf != ' + E}
FREE = '\tif (buf != ' + E + ')\n\t\tfree(buf);\n'
LOG = '\tif (verbose)\n\t\t' + NLC + '\tlog_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n' + FREE + '\treturn NULL;\n}\n'
STORE = {'size': '*len = size;', 'got': '*len = got;', 'g': 'if (len)\n\t\t\t*len = size;'}


def mk(al, g, nlg, t, st, gi):
    s = HEAD + ALLOC[al]
    if gi:
        s += '\tgot = 0;\n'
    if g == 'block':
        s += '\tif (size) {\n\t\tif (verbose)\n\t\t\t' + W + '\t}\n'
    else:
        s += '\tif (' + GUARD[g] + ')\n\t\t' + W
    if not gi:
        s += '\tgot = 0;\n'
    s += '\twhile (got < size) {\n' + LOOP
    if nlg == 'same':
        s += '\tif (' + (GUARD[g] if g != 'block' else 'verbose && size') + ')\n\t\t' + NLC
    else:
        s += '\tif (verbose)\n\t\t' + NLC
    if t == 'eq':
        s += '\tif (got == size) {\n\t\t' + STORE[st] + '\n\t\treturn buf;\n\t}\n' + LOG
    else:
        lg = LOG.rstrip()[:-1]
        s += '\tif (got != size) {\n' + lg.replace('\n\t', '\n\t\t').replace('\tif (verbose)', '\t\tif (verbose)', 1) + '\t}\n\t' + STORE[st] + '\n\treturn buf;\n}\n'
    return s


def variants():
    for al in ALLOC:
        for g in ('vs', 'sv', 'bufne', 'block'):
            for nlg in ('same', 'plain'):
                for t in ('eq', 'ne'):
                    for st in STORE:
                        for gi in (0, 1):
                            yield '|'.join((al, g, nlg, t, st, str(gi))), mk(al, g, nlg, t, st, gi)
