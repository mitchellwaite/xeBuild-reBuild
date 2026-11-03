"""Attempt 4: the flip with the plain select, crossed with sign casts at got's uses (gen_nr9's axes), since the deficit is now 50 rather than 117."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)
PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
d = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(d, 'nrhead.txt')).read()
BODY = open(os.path.join(d, 'nrbody.txt')).read()
HEAD1 = HEAD[:HEAD.index('\tif (size == 0) {')]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');"
WAIT = 'if (verbose)\n\t\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\n\tgot = 0;'
LOG = ['got, size', '(uint32_t)got, size', 'got, (uint32_t)size', '(uint32_t)got, (uint32_t)size']
LEN = ['size - got', '(int)((uint32_t)size - got)', '(int)(size - (uint32_t)got)']
EQ = ['got == size', '(uint32_t)got == (uint32_t)size']
ADD = ['got += r;', 'got += (uint32_t)r;', 'got = (uint32_t)got + r;']
ADDR = ['(char *)buf + got', '(char *)buf + (uint32_t)got']


def variants():
    for lg, ln, eq, ad, ar in itertools.product(LOG, LEN, EQ, ADD, ADDR):
        b = BODY.replace('@SEL@', PLAIN).replace('size - got', ln).replace('got += r;', ad).replace('(char *)buf + got', ar)
        t = 'if (' + eq + ') {\n\t*len = size;\n\treturn buf;\n\t}\n\t' + NL + '\n\tlog_printf(0, "received only %x of %x bytes! fail' + BS + 'n", ' + lg + ');\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'
        yield '|'.join((lg, ln, eq, ad, ar)), HEAD1 + 'if (size) {\n\tbuf = calloc(size, 1);\n\t' + WAIT + '\n\twhile (got < size) {' + b + '}\n\t' + NL + '\n\t' + t + '\n\t}\n\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n'
