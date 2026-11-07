"""Attempt 27: loadBl returning its result (`static int loadBl(e, i)`, `return -1;` / `r = -1` at fail, the caller
`r = loadBl(e, i);`) on attempt 26's and9 + c2 base (drafts/build_loadBl_c2_fail.patch, rebuilt here from src), so
that profile_estimate's return predictor sees the -1 constants in the return PHI: PRED_NEGATIVE_RETURN (98%, not taken)
on the paths to them, which is the 2% exp_pr gives the tail's `*pr` test by hand.  It only fires for a negative
INTEGER_CST of a signed type (an unsigned -1 is a positive constant: PRED_CONST_RETURN 69% the other way), so the
return type and r's type are axes.  Also: fail as `return -1;` or `r = -1; break;`, the barrier kept or off, exp_pr,
t5le and exp_t10 on or off.  Behaviour: the caller's r is 0 before the call and every path returns what *pr held.
Runs on src as of 7a9a2b41."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd370 as g0

C2 = '''		if (e->offset)
			break;
	fail:
		__asm__ __volatile__("");
		*pr = -1;
		break;
	default:'''
HEAD = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n'
CALL = '\t\t\tloadBl(e, i, &r);\n'


def c2base(b):
    """drafts/build_loadBl_c2_fail.patch: the and9 fallback, fail closing case 2, barrier kept"""
    b = g0.PRE(b)
    b = bdrun.sub(b, g0.SMC_OLD, C2, 1)
    return bdrun.sub(b, g0.END_OLD, '}\n', 1)


def ret(b, rt='int', lt='int', fl='ret'):
    """loadBl returns r (type rt; local type lt); fl: fail returns -1 itself ('ret') or sets r and breaks ('set')"""
    i = b.index(HEAD)
    j = b.index('\n}\n', i) + 3
    body = b[i:j]
    body = body.replace(HEAD, 'static %s loadBl(struct fileent *e, uint32_t i)\n{\n\tint type;\n\t%s r = 0;\n' % (rt, lt), 1)
    body = body.replace('*pr', 'r')
    if fl == 'ret':
        body = bdrun.sub(body, '\t\tr = -1;\n\t\tbreak;\n\tdefault:', '\t\treturn -1;\n\tdefault:', 1)
    body = bdrun.sub(body, '\t\tbreak;\n\t}\n}\n', '\t\tbreak;\n\t}\n\treturn r;\n}\n', 1)
    b = b[:i] + body + b[j:]
    return bdrun.sub(b, CALL, '\t\t\tr = loadBl(e, i);\n', 1)


def off(b, names):
    for n in names:
        if n == 'vol_fail':
            b = bdrun.sub(b, '\t\t__asm__ __volatile__("");\n', '', 1)
        elif n == 'exp_pr':
            b = bdrun.sub(b, '__builtin_expect(*pr != 0, 0)', '*pr != 0', 1)
        else:
            b = bdhints.off(b, n)
    return b


def mk(b, form, offs):
    b = c2base(b)
    b = off(b, offs)
    if form != 'ptr':
        rt, lt, fl = form.split('/')
        b = ret(b, rt, lt, fl)
    return b


def CASES(base):
    out = []
    forms = ['ptr', 'int/int/ret', 'int/int/set', 'int/uint32_t/ret', 'uint32_t/uint32_t/ret', 'int/uint32_t/set']
    sets = [(), ('exp_pr',), ('lab_t5le',), ('exp_pr', 'lab_t5le'), ('exp_t10',), ('vol_fail',), ('exp_pr', 'vol_fail'),
            ('exp_pr', 'lab_t5le', 'vol_fail')]
    for form, offs in itertools.product(forms, sets):
        out.append(('%s %s' % (form, '+'.join(offs) or '-'), lambda b, a=(form, offs): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
