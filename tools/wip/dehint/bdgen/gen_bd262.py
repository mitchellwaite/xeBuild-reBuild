"""Attempt 15, after gen_bd261's lab_badsize match: the same `(size & ~3) != size` spelling at the file's other two
multiple-of-4 tests (loadConsoleBlFiles' case 23, appendAddonPatches' addon test), for consistency.  BASE is
gen_bd261's `andnot` output (build/bd/gen_bd261_best.c), so run that first."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

BASE = 'build/bd/gen_bd261_best.c'
CON = ('				if (e->size & 3) {\n					log_printf(1, "\\n\\n***** ERROR: patch size',
       '				if ((e->size & ~3) != e->size) {\n					log_printf(1, "\\n\\n***** ERROR: patch size')
ADD = ('			if (!(a->size & 3)) {', '			if ((a->size & ~3) == a->size) {')


def mk(t, c, a):
    if c:
        t = bdrun.sub(t, CON[0], CON[1], 1)
    if a:
        t = bdrun.sub(t, ADD[0], ADD[1], 1)
    return t


def CASES(base):
    return [('con%d add%d' % (c, a), lambda b, c=c, a=a: mk(b, c, a)) for c, a in itertools.product((0, 1), (0, 1))]
