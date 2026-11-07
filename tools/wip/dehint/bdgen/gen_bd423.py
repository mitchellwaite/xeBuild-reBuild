"""Attempt 30: case 6 sharing the 5..21 arm by fall-through.  For type 6 the arm does exactly case 6's work (load, then
checkBl(.., 6, ..) if it loaded; none of the CF/CG, SE, signature or type-14 steps apply), so
`case 6: if (!xb.cbb) break; /* fall through */ case 5: ..` is the same behaviour, and vrp1 would thread a type-6 copy
like the reference's case 6 code.  Bases: src, and9 + c2; each with every hint kept and with each loadBl hint off, and
with the seven off.  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd410 as g0

C6 = '''	case 6:
		if (!xb.cbb)
			break;
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr)
			*pr = checkBl(e->data, e->size, 6, e->crc);
		break;
'''
ARM = '''	case 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:
'''
FT = {
    'ft': '''	case 6:
		if (!xb.cbb)
			break;
		/* fall through */
''',
    'ftg': None,
}
OFF = ['', 'exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'cp', 'etype', 'pin_d', 'off7']


def mk(b, base, form, off):
    if base == 'c2':
        b = g0.and9c2(b)
    b = bdrun.sub(b, C6, '', 1)
    if form == 'ft':
        b = bdrun.sub(b, ARM, FT['ft'] + ARM, 1)
    elif form == 'ftl':
        # case 6 as its own label inside the arm's list
        b = bdrun.sub(b, ARM, '''	case 6:
		if (!xb.cbb)
			break;
		/* fall through */
''' + ARM, 1)
    elif form == 'g':
        # case 6 placed where it was, jumping into the arm
        b = bdrun.sub(b, '''	case 24:
		/* Borderline''', '''	case 6:
		if (!xb.cbb)
			break;
		goto load;
	case 24:
		/* Borderline''', 1)
        b = bdrun.sub(b, '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {''', '''	load:
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {''', 1)
    if off == 'off7':
        return a30lib.off7(b)
    if off == 'cp':
        return bdrun.sub(b, a30lib.CPBLK, '', 1)
    if off == 'etype':
        return bdrun.sub(b, a30lib.ELSETYPE, '				} else\n', 1)
    if off:
        return bdhints.off(b, off)
    return b


def CASES(base):
    return [(' '.join(k) or '-', lambda b, k=k: mk(b, *k)) for k in itertools.product(['src', 'c2'], ['ft', 'g'], OFF)]


FOCUS = ['_loadBlFiles']
