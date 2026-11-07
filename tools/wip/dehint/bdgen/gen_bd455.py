"""Attempt 33: exp_t10 by the fallback as an inner switch (attempt 1's gen_bd18 tried a switch with 30 more hints in the
source; never on the current src or with attempt 27's weight near miss).  A switch's outgoing edges are even
(combine_predictions_for_bb only predicts two-way branches), so CG's share comes out of the switch, not of a
`type == 10` test.  Forms:
  sw     if (*pr) { switch (type) { case 9: if (suGetCF) goto se; break; case 10: if (suGetCG) goto chk; break; } break; }
  sw10   the same, case 10 first
  swd    default: break; written out
  swr    the inner switch returns instead of breaking: `if (!suGetCF) return;` (loadBl is void; the return block is the
         end of loadBl, as break is)
  ne     if (*pr) { if (type != 9 && type != 10) break; if (type == 9) {..} else {..} }
Each with src's constant_p weight and attempt 27's (`__builtin_constant_p(type) == 1`), t5le / exp_pr on and off.
Runs on src as of 5a0bc459."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']

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
		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {'''
TAIL = '''		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {'''
C9 = '''			case 9:
				if (suGetCF(&e->data, &e->size))
					goto se;
				break;
'''
C10 = '''			case 10:
				if (suGetCG(&e->data, &e->size))
					goto chk;
				break;
'''
C9R = '''			case 9:
				if (!suGetCF(&e->data, &e->size))
					return;
				goto se;
'''
C10R = '''			case 10:
				if (!suGetCG(&e->data, &e->size))
					return;
				goto chk;
'''
FORMS = {
    'sw': '\t\tif (*pr) {\n\t\t\tswitch (type) {\n' + C9 + C10 + '\t\t\t}\n\t\t\tbreak;\n\t\t}\n\tse:\n' + TAIL,
    'sw10': '\t\tif (*pr) {\n\t\t\tswitch (type) {\n' + C10 + C9 + '\t\t\t}\n\t\t\tbreak;\n\t\t}\n\tse:\n' + TAIL,
    'swd': '\t\tif (*pr) {\n\t\t\tswitch (type) {\n' + C9 + C10 + '\t\t\tdefault:\n\t\t\t\tbreak;\n\t\t\t}\n\t\t\tbreak;\n\t\t}\n\tse:\n' + TAIL,
    'swr': '\t\tif (*pr) {\n\t\t\tswitch (type) {\n' + C9R + C10R + '\t\t\t}\n\t\t\tbreak;\n\t\t}\n\tse:\n' + TAIL,
    'ne': '''		if (*pr) {
			if (type != 9 && type != 10)
				break;
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			}
		}
''' + TAIL,
}
CP_OLD = '(char *)__builtin_constant_p(type) == (char *)1'
CP_27 = '__builtin_constant_p(type) == 1'


def CASES(base):
    out = []
    for k, f in FORMS.items():
        for w in ('src', 'w27'):
            for h in ('all', 't5le', 'pr', 't5le+pr'):
                def mk(b, f=f, w=w, h=h):
                    t = bdrun.sub(b, OLD, f)
                    if w == 'w27':
                        t = bdrun.sub(t, CP_OLD, CP_27)
                    if 't5le' in h:
                        t = bdhints.off(t, 'lab_t5le')
                    if 'pr' in h:
                        t = bdhints.off(t, 'exp_pr')
                    return t
                out.append(('%s %s %s' % (k, w, h), mk))
    return out
