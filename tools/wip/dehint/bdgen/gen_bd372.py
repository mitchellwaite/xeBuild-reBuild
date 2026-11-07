"""Attempt 26, vol_fail on the and9 base (gen_bd370's PRE), barrier off: loadBl works on a local `uint32_t r = 0` in
place of *pr, and either stores it once (`*pr = r;` after the switch; fail stores -1 itself) or returns it
(`static uint32_t loadBl(e, i)`, `return r;`, fail `return -1;`, the caller `r = loadBl(e, i);`).  fail at the end
(`end`) or closing case 2 inside the switch (`c2`: `if (e->offset) break; fail: r = -1; break;`, gen_bd371's best
position).  Crossed with the tail forms.  Behaviour: the caller's r is 0 before the call, so starting from 0 is the same,
and every path ends with the same value in it.  Runs on src as of 9744ca00."""
import itertools, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd370 as g0

PRE = g0.PRE
HEAD = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n'
CALL = '\t\t\tloadBl(e, i, &r);\n'


def mk(b, mode, pos, tk, lab, exp):
    b = bdrun.sub(b, g0.TAIL_OLD, g0.tail(tk, lab, exp), 1)
    if pos == 'c2':
        b = bdrun.sub(b, g0.SMC_OLD, '''		if (e->offset)
			break;
	fail:
		*pr = -1;
		break;
	default:''', 1)
        end = {'store': '\t*pr = r;\n}\n', 'ret': '\treturn r;\n}\n'}[mode]
    else:
        end = {'store': '\t*pr = r;\n\treturn;\nfail:\n\t*pr = -1;\n}\n', 'ret': '\treturn r;\nfail:\n\treturn -1;\n}\n'}[mode]
    b = bdrun.sub(b, g0.END_OLD, end.replace('*pr = -1', 'PRM1'), 1)
    i = b.index(HEAD)
    j = b.index('\n}\n', i) + 3
    body = b[i:j]
    body = body[:len(HEAD)].replace('PRM1', '*pr = -1') + body[len(HEAD):].replace('*pr', 'r').replace('PRM1', '*pr = -1')
    if mode == 'store':
        body = body.replace('\tint type;\n', '\tint type;\n\tuint32_t r = 0;\n', 1)
    else:
        body = body.replace('static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)',
                            'static uint32_t loadBl(struct fileent *e, uint32_t i)', 1)
        body = body.replace('\tint type;\n', '\tint type;\n\tuint32_t r = 0;\n', 1)
        body = body.replace('r = -1;\n\t\tbreak;\n\tdefault:', 'return -1;\n\tdefault:')
        body = body.replace('\treturn;\n', '\treturn r;\n')
    b = b[:i] + body + b[j:]
    if mode == 'ret':
        b = bdrun.sub(b, CALL, '\t\t\tr = loadBl(e, i);\n', 1)
    return b


def CASES(base):
    out = []
    for mode, pos, (tk, lab, exp) in itertools.product(['store', 'ret'], ['end', 'c2'],
                                                      [('g', 1, 1), ('g', 0, 1), ('g', 1, 0), ('g', 0, 0), ('plain', 0, 0)]):
        out.append(('%s %s %s%s%s' % (mode, pos, tk, ' lab' if lab else '', ' exp' if exp else ''),
                    lambda b, a=(mode, pos, tk, lab, exp): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
