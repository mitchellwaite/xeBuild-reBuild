"""Attempt 6: more SSA names on got's base through a PHI: shared exits that read got (got = 0 on the zero path, one *len = got),
and the attempt-2 flag loops redone on the flip."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
i = FLIP.index('\t\tif (got == size) {')
PRE, TAIL = FLIP[:i], FLIP[i:]
j = PRE.index('\tif (size) {')
HEAD, XFER = PRE[:j], PRE[j + len('\tif (size) {\n'):]
NL = "if (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\t"
FAIL = NL + 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\treturn NULL;\n'
X2 = XFER.replace('got = 0;', '')


def shared():
    # store variable, got's init place
    for store in ('got', 'size'):
        ret = '\t*len = %s;\n\treturn buf;\n}\n\n' % store
        yield 'dflt-both|' + store, HEAD + '\tgot = 0;\n\tbuf = (uint8_t *)&netEmpty;\n\tif (size) {\n' + X2 + '\t\tif (got != size) {\n\t\t' + FAIL + '\t\t}\n\t}\n' + ret
        yield 'dflt-reinit|' + store, HEAD + '\tgot = 0;\n\tbuf = (uint8_t *)&netEmpty;\n\tif (size) {\n' + XFER + '\t\tif (got != size) {\n\t\t' + FAIL + '\t\t}\n\t}\n' + ret
        yield 'else|' + store, HEAD + '\tif (!size) {\n\t\tgot = 0;\n\t\tbuf = (uint8_t *)&netEmpty;\n\t} else {\n' + XFER + '\t\tif (got != size) {\n\t\t' + FAIL + '\t\t}\n\t}\n' + ret
        yield 'goto|' + store, HEAD + '\tgot = 0;\n\tbuf = (uint8_t *)&netEmpty;\n\tif (size) {\n' + X2 + '\t\tif (got == size)\n\t\t\tgoto done;\n\t\t' + FAIL + '\t}\ndone:\n' + ret
        yield 'nest|' + store, HEAD + '\tgot = 0;\n\tif (size) {\n' + X2 + '\t\tif (got == size) {\n\t\t\t*len = %s;\n\t\t\treturn buf;\n\t\t}\n\t\t' % store + FAIL + '\t}\n\t*len = got;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
    yield 'zero-got', rep(FLIP, ('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;', '\tgot = 0;\n\t*len = got;\n\treturn (uint8_t *)&netEmpty;'))
    yield 'head-got', rep(FLIP, ('\t*len = 0;\n\tr = select', '\tgot = 0;\n\t*len = got;\n\tr = select'), ('\t\tgot = 0;\n', ''))


def flags():
    SLOG = '\t\t\t\tlog_printf(0, "timeout waiting for data, error %d' + BS + 'n", WSAGetLastError());\n'
    A = SLOG + '\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;\n'
    RL = '\t\t\t\t\t   WSAGetLastError());\n'
    B = RL + '\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;\n'
    F = '\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\treturn NULL;\n'
    for sn, sel in (('plain', None), ('side', 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {')):
        base = FLIP if not sel else rep(FLIP, (SEL, sel))
        for var, val in (('err', '1'), ('ok', '0')):
            d = rep(base, ('int size, got, r;', 'int size, got, r, %s = %s;' % (var, '0' if var == 'err' else '1')))
            t = '\t\tif (%s) {\n' % (var if var == 'err' else '!ok')
            yield 'break-tail|%s|%s' % (var, sn), rep(d, (A, SLOG + '\t\t\t\t%s = %s;\n\t\t\t\tbreak;\n' % (var, val)), (B, RL + '\t\t\t\t%s = %s;\n\t\t\t\tbreak;\n' % (var, val)),
                                                  ('\t\t}\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)', '\t\t}\n' + t + F + '\t\t}\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)'))
            cond = 'got < size && ok' if var == 'ok' else 'got < size && !err'
            yield 'cont-cond|%s|%s' % (var, sn), rep(d, (A, SLOG + '\t\t\t\t%s = %s;\n\t\t\t\tcontinue;\n' % (var, val)), (B, RL + '\t\t\t\t%s = %s;\n\t\t\t\tcontinue;\n' % (var, val)), ('while (got < size)', 'while (' + cond + ')'),
                                                 ('\t\t}\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)', '\t\t}\n' + t + F + '\t\t}\n\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tif (got == size)'))


def variants():
    yield from shared()
    yield from flags()
