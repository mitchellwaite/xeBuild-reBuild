"""Attempt 4: the flip (transfer nested under if (size), zero case after it): V=0 with the plain select. Cross it with what gave the clone's registers before: guards, bottom exits, tails, type of got."""
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
STORE = '*len = size;\n\treturn buf;'
LOOP = {
    'while': lambda b: 'while (got < size) {' + b + '}',
    'dogt': lambda b: 'if (size > 0) do {' + b + '} while (got < size);',
    'whilege': lambda b: 'while (got < size) {' + b + 'if (got >= size)\n\t\t\tbreak;\n\t}',
    'whilegt': lambda b: 'while (got < size) {' + b + 'if (got > size)\n\t\t\tbreak;\n\t}',
    'ifwhile': lambda b: 'if (size > 0) {\n\twhile (got < size) {' + b + '}\n\t}',
    'dobreak': lambda b: 'if (size > 0) for (;;) {' + b + 'if (got >= size)\n\t\t\tbreak;\n\t}',
}
TAIL = {
    'eq': 'if (got == size) {\n\t' + STORE + '\n\t}\n\t' + FAIL,
    'ne': 'if (got != size) {\n\t' + FAIL + '\n\t}\n\t' + STORE,
    'eqelse': 'if (got == size) {\n\t' + STORE + '\n\t} else {\n\t' + FAIL + '\n\t}',
}
OUTER = {'if': 'if (size) {', 'ne': 'if (size != 0) {'}
ZERO = {'lit': '*len = 0;\n\treturn (uint8_t *)&netEmpty;', 'size': '*len = size;\n\treturn (uint8_t *)&netEmpty;', 'nolen': 'return (uint8_t *)&netEmpty;'}
DECL = {'int': None, 'long': 'long size, got, r;'}


def variants():
    for (lk, lf), (tk, t), (ok, o), (zk, z), (sk, s) in itertools.product(LOOP.items(), TAIL.items(), OUTER.items(), ZERO.items(), (('plain', PLAIN), ('side', SIDE))):
        yield '%s|%s|%s|%s|%s' % (lk, tk, ok, zk, sk), HEAD1 + o + '\n\tbuf = calloc(size, 1);\n\t' + WAIT + '\n\t' + lf(BODY.replace('@SEL@', s)) + '\n\t' + NL + '\n\t' + t + '\n\t}\n\t' + z + '\n}\n'
