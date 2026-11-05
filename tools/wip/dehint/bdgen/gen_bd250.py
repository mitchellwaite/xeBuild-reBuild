"""Attempt 14: loadBl's tail as `if (xb.type > BUILD_DEVGL16 && type == 14)` (the Linux build's reading), crossed with
the size log's -1 (goto fail or its own), the fail barrier, and the forms of the `*pr` test after the kit arm.
Runs on src/build.c as of eb75581."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
SIZE_SRC = ('		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			goto fail;\n		}\n')
TAIL_SRC = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
            '				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n')
SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
AND = '		if (xb.type > BUILD_DEVGL16 && type == 14) {\n			' + SET + '			break;\n		}\n'
NEST = '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '			break;\n		}\n'

TAILS = {
    'src': TAIL_SRC,
    'and_exp': AND + '		if (__builtin_expect(*pr != 0, 0))\n			goto fail;\n		break;\n',
    'and_pl': AND + '		if (*pr)\n			goto fail;\n		break;\n',
    'and_none': '		if (xb.type > BUILD_DEVGL16 && type == 14)\n			' + SET + '		break;\n',
    'nest_exp': NEST + '		if (__builtin_expect(*pr != 0, 0))\n			goto fail;\n		break;\n',
    'nest_pl': NEST + '		if (*pr)\n			goto fail;\n		break;\n',
    # sig-failed state carried in *pr, -1 set only at fail
    'and_eq': AND + '		if (*pr == -1)\n			goto fail;\n		break;\n',
}
SIZE = {
    'g': SIZE_SRC,
    'b': '		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			*pr = -1;\n			break;\n		}\n',
}


def mk(t, tail, size, vol):
    t = bdrun.sub(t, TAIL_SRC, TAILS[tail], 1)
    t = bdrun.sub(t, SIZE_SRC, SIZE[size], 1)
    if vol == 'nv':
        t = bdhints.off(t, 'vol_fail')
    return t


def CASES(base):
    out = []
    for tail, size, vol in itertools.product(TAILS, SIZE, ('v', 'nv')):
        out.append(('%s %s %s' % (tail, size, vol), lambda b, a=tail, s=size, v=vol: mk(b, a, s, v)))
    return out


FOCUS = ['_loadBlFiles']
