"""Attempt 45: the update fallback's forms on the loop-form near miss (n1: a45lib.loop fb=con2 sz=and3, etype + cp +
lab_t5le off), crossed with exp_t10 / exp_pr / vol_fail off.  The only line left on n1 is case 24's r = 1 block, which
follows the suGetCF block (freq 41 against its 32) in bbro's round 4; these forms move the CF block's frequency.
`BDEXTRA='--param builtin-expect-probability=99' python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd562.py -n 300`."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a45lib
from a45lib import loop

FOCUS = None
L = '		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n'
X10 = '__builtin_expect(type == 10, 0)'
a45lib.FBX.update({
    # console's own form: the SE test and checkBl under `if (!r)`
    'con': L + '''		if (r) {
			if (type == 9) {
				if (suGetCF(&e->data, &e->size))
					r = 0;
			} else if (X10) {
				if (suGetCG(&e->data, &e->size))
					r = 0;
			}
		}
		if (r)
			break;
SE
''',
    # flat && tests
    'and': L + '''		if (r && type == 9 && suGetCF(&e->data, &e->size))
			r = 0;
		if (r && X10 && suGetCG(&e->data, &e->size))
			r = 0;
		if (r)
			break;
''',
    'andelse': L + '''		if (r && type == 9 && suGetCF(&e->data, &e->size))
			r = 0;
		else if (r && X10 && suGetCG(&e->data, &e->size))
			r = 0;
		if (r)
			break;
''',
    'nest_and': L + '''		if (r) {
			if (type == 9 && suGetCF(&e->data, &e->size))
				r = 0;
			else if (X10 && suGetCG(&e->data, &e->size))
				r = 0;
		}
		if (r)
			break;
''',
    'sw': L + '''		if (r) {
			switch (type) {
			case 9:
				if (suGetCF(&e->data, &e->size))
					r = 0;
				break;
			case 10:
				if (suGetCG(&e->data, &e->size))
					r = 0;
				break;
			}
		}
		if (r)
			break;
''',
    # good fallbacks rejoin through r, the failures break at once
    'brk': L + '''		if (r) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (X10) {
				if (!suGetCG(&e->data, &e->size))
					break;
			} else
				break;
			r = 0;
		}
''',
    'con2': L + '''		if (r) {
			if (type == 9) {
				if (suGetCF(&e->data, &e->size))
					r = 0;
			} else if (X10) {
				if (suGetCG(&e->data, &e->size))
					r = 0;
			}
		}
		if (r)
			break;
''',
    'con2n': L + '''		if (r != 0) {
			if (type == 9) {
				if (suGetCF(&e->data, &e->size) != 0)
					r = 0;
			} else if (X10) {
				if (suGetCG(&e->data, &e->size) != 0)
					r = 0;
			}
		}
		if (r != 0)
			break;
''',
})
for k in list(a45lib.FBX):
    a45lib.FBX[k] = a45lib.FBX[k].replace('X10', X10)
BASEOFF = ('etype', 'cp', 'lab_t5le')


def CASES(base):
    out = []
    for fb, fail, tail in itertools.product(['con2', 'con', 'and', 'andelse', 'nest_and', 'sw', 'brk', 'con2n'], ['c2', 'each'],
                                            ['src', 'plain']):
        extra = [(), ('exp_t10',)]
        if tail == 'src':
            extra += [('exp_pr',), ('exp_t10', 'exp_pr')]
        if fail == 'c2':
            extra += [e + ('vol_fail',) for e in list(extra)]
        for ex in extra:
            if fb == 'sw' and 'exp_t10' not in ex:
                continue
            off = tuple(o for o in BASEOFF if not (o == 'lab_t5le' and tail != 'src')) + ex
            off2 = off if fb != 'sw' else tuple(o for o in off if o != 'exp_t10')
            lab = '%s %s %s|%s' % (fb, fail, tail, '+'.join(ex) or '-')
            out.append((lab, lambda t, kw=dict(fb=fb, sz='and3', fail=fail, tail=tail, off=off2): loop(t, **kw)))
    return out
