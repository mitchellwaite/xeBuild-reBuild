"""Attempt 30: base B30 = loadBl returning a local `uint32_t r` (caller `r = loadBl(e, i);`), the and9 fallback, fail
closing case 2, the plain tail (`if (xb.type <= BUILD_DEVGL16) break;`), `else if (type)` kept (gen_bd412 `retu and9 src
plain 1`: 35 loose, no displacement).  Put loadBl's other hints back one or more at a time to see which difference each
one owns on B30: vol (the barrier at fail), cp (the constant_p entry, src's weight), t10 (exp_t10), tail (src's tail
with t5le and exp_pr, or without them).  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
import gen_bd411 as g
import gen_bd412 as g2


def B30(b):
    return g2.mk(b, 'retu', 'and9', 'src', 'plain', 1)


PLAIN = '''		if (xb.type <= BUILD_DEVGL16)
			break;
		if (type == 14)
'''
TAILS = {
    'plain': PLAIN,
    'src': '''		if (xb.type <= BUILD_DEVGL16) {
			if (r != 0)
				goto fail;
			break;
		}
		if (type == 14)
''',
    'srcH': '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(r != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
''',
}
CP = '''		log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
		if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {
			type = (type & 1) + 18;
			goto chk;
		}
'''
DEF = '''		log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
'''
FAIL = '''	fail:
		r = -1;
'''


def mk(b, vol, cp, t10, tail):
    b = B30(b)
    if vol:
        b = bdrun.sub(b, FAIL, '\tfail:\n\t\t__asm__ __volatile__("");\n\t\tr = -1;\n', 1)
    if cp:
        b = bdrun.sub(b, DEF, CP, 1)
    if t10:
        b = bdrun.sub(b, 'else if (type == 10 && suGetCG', 'else if (__builtin_expect(type == 10, 0) && suGetCG', 1)
    b = bdrun.sub(b, PLAIN, TAILS[tail], 1)
    return b


PRE = g.PRE


def CASES(base):
    return [(' '.join(map(str, k)), lambda b, k=k: mk(b, *k))
            for k in itertools.product([0, 1], [0, 1], [0, 1], list(TAILS))]


FOCUS = ['_loadBlFiles']
