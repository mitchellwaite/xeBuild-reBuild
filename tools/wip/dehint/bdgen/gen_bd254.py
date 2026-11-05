"""Attempt 14: loadBl's signature test as a switch, the way verifyBlSigs writes the same test (`case 5: case 11:
case 17:`).  Axes: case order, the passed arm (`else if (type)` or plain else), loadBl's other hints on or off.
Runs on src/build.c as of eb75581."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

HEAD = '		if (type == 5 || type == 17 || type == 11) {\n'
ELSE = ('				/* Borderline, for review: type is 5, 11 or 17 here, so this test\n'
        '				   is always true; a plain else costs 54 lines */\n				} else if (type)\n')
END = ('				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n		}\n')
CP_SRC = '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1'
ORD = {'5_11_17': (5, 11, 17), '17_5_11': (17, 5, 11), '5_17_11': (5, 17, 11), '11_5_17': (11, 5, 17)}


def mk(t, o, el, hints):
    cases = ' '.join('case %d:' % c for c in ORD[o])
    t = bdrun.sub(t, HEAD, '		switch (type) {\n		' + cases + '\n', 1)
    if el == 'else':
        t = bdrun.sub(t, ELSE, '				} else\n', 1)
    if hints == 'nocp':
        t = bdrun.sub(t, CP_SRC, '0', 1)
    elif hints == 'nocpl':
        t = bdrun.sub(t, CP_SRC, '0', 1)
        t = bdhints.off(t, 'lab_t5le')
    elif hints == 'nol':
        t = bdhints.off(t, 'lab_t5le')
    return t


def CASES(base):
    out = []
    for o, el, h in itertools.product(ORD, ('type', 'else'), ('all', 'nol', 'nocp', 'nocpl')):
        out.append(('%s %s %s' % (o, el, h), lambda b, o=o, e=el, h=h: mk(b, o, e, h)))
    return out


FOCUS = ['_loadBlFiles']
