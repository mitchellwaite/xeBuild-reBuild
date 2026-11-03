"""Attempt 4: lever 1: the do family with the flip under head shapes that change the entry frequency, to see if the round thresholds move log or J later. Needs nrhead.txt/nrbody.txt."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)
PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
d = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(d, 'nrhead.txt')).read()
BODY = open(os.path.join(d, 'nrbody.txt')).read()
A = HEAD.index('\tsize = getBeU32(hdr);')
HEAD0 = HEAD[:A]
NL = "if (verbose)\n\t\tputchar('" + BS + "n');"
WAIT = 'if (verbose)\n\t\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\n\tgot = 0;'
FAIL = NL + '\n\tlog_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'
STORE = '*len = size;\n\treturn buf;'
Z = '*len = 0;\n\treturn (uint8_t *)&netEmpty;'
LOOP = {
    'while': lambda b: 'while (got < size) {' + b + '}',
    'dogt': lambda b: 'if (size > 0) do {' + b + '} while (got < size);',
    'ifwhile': lambda b: 'if (size > 0) {\n\twhile (got < size) {' + b + '}\n\t}',
}
TAIL = {'eq': 'if (got == size) {\n\t' + STORE + '\n\t}\n\t' + FAIL, 'ne': 'if (got != size) {\n\t' + FAIL + '\n\t}\n\t' + STORE}


def wrap(h, x):
    g = 'size = getBeU32(hdr);\n\t'
    if h == 'flip':
        return g + 'if (size == -1)\n\t\treturn NULL;\n\tif (size) {\n\t' + x + '\n\t}\n\t' + Z
    if h == 'flip2':   # -1 tested inside the nonzero arm
        return g + 'if (size) {\n\tif (size == -1)\n\t\treturn NULL;\n\t' + x + '\n\t}\n\t' + Z
    if h == 'flip3':   # -1 tested last
        return g + 'if (size != -1) {\n\tif (size) {\n\t' + x + '\n\t}\n\t' + Z + '\n\t}\n\treturn NULL;'
    if h == 'flip4':   # zero arm first, else
        return g + 'if (size == -1)\n\t\treturn NULL;\n\tif (size == 0) {\n\t' + Z + '\n\t} else {\n\t' + x + '\n\t}'
    if h == 'flip5':
        return g + 'if (size != -1 && size != 0) {\n\t' + x + '\n\t}\n\tif (size == -1)\n\t\treturn NULL;\n\t' + Z


def variants():
    for h, (lk, lf), (tk, t) in itertools.product(('flip', 'flip2', 'flip3', 'flip4', 'flip5'), LOOP.items(), TAIL.items()):
        x = 'buf = calloc(size, 1);\n\t' + WAIT + '\n\t' + lf(BODY.replace('@SEL@', PLAIN)) + '\n\t' + NL + '\n\t' + t
        yield '%s|%s|%s' % (h, lk, tk), HEAD0 + wrap(h, x) + '\n}\n'
