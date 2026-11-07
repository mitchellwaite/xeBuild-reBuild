"""Attempt 25: gen_bd360's `and9` family (the CF-failure path goes on to the `type == 10` test; IDENTICAL with the
expect, and it halves vol_fail's cost) crossed with loadBl's tail forms: src's (`if (*pr) goto fail;` under the
`<= 5` test, with or without t5le / exp_pr), attempt 10's plain `if (xb.type <= BUILD_DEVGL16) break;` (the goto is a
no-op: *pr is 0 there or already -1), the size error through `goto fail` or `*pr = -1; break;`, and the barrier.
Runs on src as of 3778d12d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
CF = 'suGetCF(&e->data, &e->size)'
CG = 'suGetCG(&e->data, &e->size)'
T10 = '__builtin_expect(type == 10, 0)'
FB = {
    'src': OLD,
    'and9': '''		if (*pr) {
			if (type == 9 && %s)
				;
			else if (T10 && %s)
				goto chk;
			else
				break;
		}
''' % (CF, CG),
    'nest9': '''		if (*pr) {
			if (type != 9 || !%s) {
				if (!(T10) || !%s)
					break;
				goto chk;
			}
		}
''' % (CF, CG),
    'nogo': '''		if (*pr) {
			if (!(type == 9 && %s) && !(T10 && %s))
				break;
		}
''' % (CF, CG),
}
TAILOLD = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
TAIL = {
    'src': TAILOLD,
    'not5le': TAILOLD.replace('\t\tt5le: __attribute__((hot));\n', ''),
    'nopr': TAILOLD.replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    'none': TAILOLD.replace('\t\tt5le: __attribute__((hot));\n', '').replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    'plain': '''		if (xb.type <= BUILD_DEVGL16)
			break;
''',
}
LOG = '\t\t\tlog_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
SIZE = {'fail': None, 'brk': (LOG + '\t\t\tgoto fail;\n', LOG + '\t\t\t*pr = -1;\n\t\t\tbreak;\n')}
BAR = {'bar': None, 'nobar': ('fail:\n\t__asm__ __volatile__("");\n', 'fail:\n')}
T10S = {'t10': T10, 'not10': 'type == 10'}


def mk(b, f, t10, tl, sz, br):
    b = bdrun.sub(b, OLD, FB[f].replace('T10', T10).replace(T10, T10S[t10]), 1)
    b = bdrun.sub(b, TAILOLD, TAIL[tl], 1)
    if SIZE[sz]:
        b = bdrun.sub(b, SIZE[sz][0], SIZE[sz][1], 1)
    if BAR[br]:
        b = bdrun.sub(b, BAR[br][0], BAR[br][1], 1)
    return b


def CASES(base):
    out = []
    for f, t10, tl, sz, br in itertools.product(FB, T10S, TAIL, SIZE, BAR):
        if f == 'src' and t10 == 'not10':
            pass
        out.append(('%s %s %s %s %s' % (f, t10, tl, sz, br), lambda b, a=(f, t10, tl, sz, br): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
