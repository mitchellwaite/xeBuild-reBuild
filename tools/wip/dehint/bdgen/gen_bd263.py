"""Attempt 15: gen_bd261's lever (a spelling that picks an opcode heuristic) on loadBl's tail.  `*pr` is 0 or -1 at the
`xb.type <= BUILD_DEVGL16` tail, so `*pr == -1` (nonequal) and `(int)*pr < 0` (positive) test the same thing as
`*pr != 0`.  Axes: the `*pr` test's spelling, with or without its expect, with or without the t5le label, and the
tail's `xb.type` test spelling.  Runs on src/build.c after the lab_badsize landing."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

PR_OLD = '			if (__builtin_expect(*pr != 0, 0))\n'
PR = {
    'exp': PR_OLD,
    'ne0': '			if (*pr != 0)\n',
    'eqm1': '			if (*pr == -1)\n',
    'eqm1u': '			if (*pr == (uint32_t)-1)\n',
    'neg': '			if ((int)*pr < 0)\n',
    'eqm1x': '			if (__builtin_expect(*pr == -1, 0))\n',
}
T5_OLD = '		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n'
T5 = {
    'lab': T5_OLD,
    'plain': '		if (xb.type <= BUILD_DEVGL16) {\n',
    'lt6': '		if (xb.type < BUILD_DEVKIT) {\n',
}


def mk(t, p, l):
    t = bdrun.sub(t, PR_OLD, PR[p], 1)
    t = bdrun.sub(t, T5_OLD, T5[l], 1)
    return t


def CASES(base):
    out = []
    for p, l in itertools.product(PR, T5):
        if p == 'exp' and l == 'lab':
            continue
        out.append(('%s %s' % (p, l), lambda b, p=p, l=l: mk(b, p, l)))
    return out


FOCUS = ['_loadBlFiles']
