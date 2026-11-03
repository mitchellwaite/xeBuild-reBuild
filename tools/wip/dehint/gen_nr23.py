"""Attempt 4: guard x tail in the do family. Targets from the arithmetic: else in (130,187), P(fail) .62 from `if (got != size) {...; return NULL;}`. Guards with goto/early return predictors."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)
PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
SIDE = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'
HEAD = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nrhead.txt')).read()
BODY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nrbody.txt')).read()
NL = "if (verbose)\n\t\tputchar('" + BS + "n');"
FAIL = NL + '\n\tlog_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'
STORE = '*len = size;\n\treturn buf;'
LOOPS = {
    'do': lambda b: 'if (size > 0) do {' + b + '} while (got < size);',
    'do2': lambda b: 'if (size > 0) {\n\t\tdo {' + b + '} while (got < size);\n\t}',
    'gotoafter': lambda b: 'if (size <= 0)\n\t\tgoto done;\n\tdo {' + b + '} while (got < size);\ndone:',
    'gotoafterlt': lambda b: 'if (size < 1)\n\t\tgoto done;\n\tdo {' + b + '} while (got < size);\ndone:',
    'gotoloop': lambda b: 'if (size > 0)\n\t\tgoto recvloop;\n\tgoto done;\nrecvloop:\n\tdo {' + b + '} while (got < size);\ndone:',
    'forever': lambda b: 'if (size > 0) {\n\t\tfor (;;) {' + b + 'if (got >= size)\n\t\t\tbreak;\n\t\t}\n\t}',
    'while': lambda b: 'while (got < size) {' + b + '}',
    'ifwhile': lambda b: 'if (size > 0) {\n\t\twhile (got < size) {' + b + '}\n\t}',
}
TAILS = {
    'ne': NL + '\n\tif (got != size) {\n\t' + FAIL + '\n\t}\n\t' + STORE,
    'eq': NL + '\n\tif (got == size) {\n\t' + STORE + '\n\t}\n\t' + FAIL,
    'eqelse': NL + '\n\tif (got == size) {\n\t' + STORE + '\n\t} else {\n\t' + FAIL + '\n\t}',
    'neret': NL + '\n\tif (got != size)\n\t\tgoto fail;\n\t' + STORE + '\nfail:\n\t' + FAIL,
}


def variants():
    for (lk, lf), (tk, t), (sk, s) in itertools.product(LOOPS.items(), TAILS.items(), (('plain', PLAIN), ('side', SIDE))):
        yield '%s|%s|%s' % (lk, tk, sk), HEAD + lf(BODY.replace('@SEL@', s)) + '\n\t' + t + '\n}\n'
