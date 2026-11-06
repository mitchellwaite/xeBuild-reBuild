"""Attempt 15: attempt 10's brktail near miss (no asm, no t5le label, no `*pr` expect) on the source after the
lab_badsize landing, whose size test now gets the nonequal heuristic.  Axes: the tail's `*pr` handling (plain break as
the near miss, or `*pr == -1` kept), the size log's exit (`*pr = -1; break;` or `goto fail`), the barrier.
Runs on src/build.c after the lab_badsize landing."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
TAILS = {
    'src': TAIL,
    'brk': '''		if (xb.type <= BUILD_DEVGL16)
			break;
''',
    'eqm1': '''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr == -1)
				goto fail;
			break;
		}
''',
    'eqm1l': '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (*pr == -1)
				goto fail;
			break;
		}
''',
}
SZ = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
'''
SZS = {
    'goto': SZ,
    'brk': SZ.replace('			goto fail;\n', '			*pr = -1;\n			break;\n'),
}
BAR = '	__asm__ __volatile__("");\n	*pr = -1;\n}\n'


def mk(t, ta, sz, bar):
    t = bdrun.sub(t, TAIL, TAILS[ta], 1)
    t = bdrun.sub(t, SZ, SZS[sz], 1)
    if not bar:
        t = bdrun.sub(t, BAR, '	*pr = -1;\n}\n', 1)
    return t


def CASES(base):
    out = []
    for ta, sz, bar in itertools.product(TAILS, SZS, (1, 0)):
        if (ta, sz, bar) == ('src', 'goto', 1):
            continue
        out.append(('%s %s bar%d' % (ta, sz, bar), lambda b, ta=ta, sz=sz, bar=bar: mk(b, ta, sz, bar)))
    return out


FOCUS = ['_loadBlFiles']
