"""Attempt 15, exp_verbose (+ pin_e): gen_bd261's lever on loadFileCrc.  The bytes log needs the equal case hotter;
`size != e->size` gets nonequal (72% for the pad log).  Forms that compare with 0 get no heuristic, if fold leaves them
alone.  Axes: the size compare's spelling x the verbose test's spelling x pin_e.  Runs on src/build.c after the
lab_badsize landing."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

V_OLD = '	if (__builtin_expect(verbose, 1)) {\n		if (size != e->size) {\n'
CMP = {
    'ne': 'size != e->size',
    'sub': 'size - e->size',
    'sub0': 'size - e->size != 0',
    'rsub': 'e->size - size',
    'xor': 'size ^ e->size',
    'gt': 'e->size > size',
    'lt': 'size < e->size',
}
VB = {'plain': 'verbose', 'gt0': 'verbose > 0', 'ne0': 'verbose != 0'}


def mk(t, c, v, pin):
    t = bdrun.sub(t, V_OLD, '	if (%s) {\n		if (%s) {\n' % (VB[v], CMP[c]), 1)
    if not pin:
        t = bdhints.off(t, 'pin_e')
    return t


def CASES(base):
    return [('%s %s pin%d' % (c, v, p), lambda b, c=c, v=v, p=p: mk(b, c, v, p))
            for c, v, p in itertools.product(CMP, VB, (1, 0))]


FOCUS = ['_loadFileCrc', '_loadCommonFile']
