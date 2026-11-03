"""Attempt 4: why buf != &netEmpty exists: size 0 flows through to one store, with buf defaulting to &netEmpty and the transfer nested under if (size). The reference's redundant *len = 0 could be that store with size 0 propagated."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)
PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
SIDE = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'
d = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(d, 'nrhead.txt')).read()
BODY = open(os.path.join(d, 'nrbody.txt')).read()
HEAD1 = HEAD[:HEAD.index('\tif (size == 0) {')]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');"
WAIT = 'if (verbose)\n\t\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\n\tgot = 0;'
FAIL = NL + '\n\tlog_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'
LOOP = {'while': lambda b: 'while (got < size) {' + b + '}', 'do': lambda b: 'do {' + b + '} while (got < size);'}


def shape(k, loop):
    xfer = 'buf = calloc(size, 1);\n\t' + WAIT + '\n\t' + loop + '\n\t' + NL + '\n\t'
    if k == 'share_ne':
        return 'buf = (uint8_t *)&netEmpty;\n\tif (size) {\n\t' + xfer + 'if (got != size) {\n\t' + FAIL + '\n\t}\n\t}\n\t*len = size;\n\treturn buf;\n}\n'
    if k == 'share_eq':
        return 'buf = (uint8_t *)&netEmpty;\n\tif (size) {\n\t' + xfer + 'if (got == size)\n\t\tgoto ok;\n\t' + FAIL + '\n\t}\nok:\n\t*len = size;\n\treturn buf;\n}\n'
    if k == 'flip':
        return 'if (size) {\n\t' + xfer + 'if (got == size) {\n\t*len = size;\n\treturn buf;\n\t}\n\t' + FAIL + '\n\t}\n\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n'
    if k == 'else':
        return 'if (size == 0)\n\t\tbuf = (uint8_t *)&netEmpty;\n\telse {\n\t' + xfer + 'if (got != size) {\n\t' + FAIL + '\n\t}\n\t}\n\t*len = size;\n\treturn buf;\n}\n'


def variants():
    for k, (lk, lf), (sk, s) in itertools.product(('share_ne', 'share_eq', 'flip', 'else'), LOOP.items(), (('plain', PLAIN), ('side', SIDE))):
        yield '%s|%s|%s' % (k, lk, sk), HEAD1 + shape(k, lf(BODY.replace('@SEL@', s)))
