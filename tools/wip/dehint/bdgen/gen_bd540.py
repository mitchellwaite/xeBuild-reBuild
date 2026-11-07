"""Attempt 42: pair and triple removal sweep (hint interactions).  Every pair of the 9 removable items (bdhints' 7 plus
`etype` = the plain else and `cp` = the constant_p entry as `if (0)`) on src, and every single / pair / triple of the 6
loadBl-side items on the near-miss bases: `and9` (attempt 25's fallback), `c2` (and9 + fail closing case 2, barrier
kept), `c6` (c2 + case 6 first), `noi` (gen_bd521: edata, the entry's first term on e->crc, loadBl without i), `wt`
(attempt 27's weight: the entry's second compare as `__builtin_constant_p(type) == 1`).
BDBASES=src,and9 (default all) and BDDEPTH=2|3 (default 3) narrow it.  Runs on src as of 92fa270c.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd540.py -n 1000`."""
import itertools, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = None

FB_OLD = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
FB_AND9 = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
C2_OLD = '''		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			goto fail;
		break;
	default:'''
C2_NEW = '''		e->offset = smcSetLoad(e->size);
		if (e->offset)
			break;
	fail:
		__asm__ __volatile__("");
		*pr = -1;
		break;
	default:'''
TAIL_OLD = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}'''
C6 = '''	case 6:
		if (!xb.cbb)
			break;
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr)
			*pr = checkBl(e->data, e->size, 6, e->crc);
		break;
'''
CP = '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1'
LB_HEAD = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)'


def and9(t):
    return bdrun.sub(t, FB_OLD, FB_AND9, 1)


def c2(t):
    t = bdrun.sub(and9(t), C2_OLD, C2_NEW, 1)
    return bdrun.sub(t, TAIL_OLD, '}', 1)


def c6(t):
    t = c2(t)
    t = bdrun.sub(t, C6, '', 1)
    return bdrun.sub(t, '\tswitch (type) {\n\tcase 5:', '\tswitch (type) {\n' + C6 + '\tcase 5:', 1)


def noi(t):
    t = bdrun.sub(t, 'setFlashBuild(getBeU16(xb.files[i].data + 2));', 'setFlashBuild(getBeU16(e->data + 2));', 1)
    t = bdrun.sub(t, CP, CP.replace('(i)', '(e->crc)'), 1)
    t = bdrun.sub(t, LB_HEAD, LB_HEAD.replace('uint32_t i, ', ''), 1)
    return bdrun.sub(t, 'loadBl(e, i, &r);', 'loadBl(e, &r);', 1)


def wt(t):
    return bdrun.sub(t, CP, CP.replace('(char *)__builtin_constant_p(type) == (char *)1', '__builtin_constant_p(type) == 1'), 1)


BASES = {'src': lambda t: t, 'and9': and9, 'c2': c2, 'c6': c6, 'noi': noi, 'wt': wt}
LB = ['exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'etype', 'cp']
ALL = LB + ['lab_none', 'pin_size', 'exp_devgl']


def off(t, k):
    if k == 'etype':
        return bdrun.sub(t, '\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n', 1)
    if k == 'cp':
        t2 = re.sub(r'if \(\(char \*\)__builtin_constant_p\([^)]*\) == \(char \*\)1 && [^{]*\) \{', 'if (0) {', t, 1)
        if t2 == t:
            raise ValueError('cp not found')
        return t2
    return bdhints.off(t, k)


def offs(t, ks):
    for k in ks:
        t = off(t, k)
    return t


def CASES(base):
    out = []
    depth = int(os.environ.get('BDDEPTH', '3'))
    for b in os.environ.get('BDBASES', ','.join(BASES)).split(','):
        f = BASES[b]
        items = ALL if b == 'src' else LB
        sets = [()]
        for n in range(1, depth + 1):
            if n == 3:
                sets += list(itertools.combinations(LB, 3))
            else:
                sets += list(itertools.combinations(items, n))
        for s in sets:
            out.append(('%s|%s' % (b, '+'.join(s) or 'none'), lambda t, f=f, s=s: offs(f(t), s)))
    return out
