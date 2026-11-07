"""Attempt 26, vol_fail on attempt 25's and9 base (the update fallback as `if (type == 9 && CF) ; else if (type == 10 && CG)
goto chk; else break;`, type == 10 expect kept; IDENTICAL with the barrier, 60 loose without).  The barrier is off in
every case.  Axes: each of fail's three sources (the patch size log, case 2's smcSetLoad test, the signature tail's
`if (*pr) goto fail`) either goes to fail or sets -1 itself (`*pr = -1; break;` / `return;`, the tail as a plain break
since *pr is already 0 or -1 there); the tail's t5le label and `*pr` expect on or off; and a `bad` flag mode, where each
source sets `bad = 1` and one `if (bad) *pr = -1;` after the switch replaces the label.  Behaviour is the same in all:
the three failures end with *pr == -1, every other path leaves *pr as it was.  Runs on src as of 9744ca00."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

AND9_OLD = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
AND9 = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
LOG = '\t\t\tlog_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
SIZE_OLD = LOG + '\t\t\tgoto fail;\n'
SMC_OLD = '''		if (!e->offset)
			goto fail;
		break;
	default:'''
TAIL_OLD = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
END_OLD = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''


def PRE(b):
    return bdrun.sub(b, AND9_OLD, AND9, 1)


SIZE = {'g': SIZE_OLD, 'brk': LOG + '\t\t\t*pr = -1;\n\t\t\tbreak;\n', 'ret': LOG + '\t\t\t*pr = -1;\n\t\t\treturn;\n'}
SMC = {'g': SMC_OLD, 'own': SMC_OLD.replace('goto fail;', '*pr = -1;'),
       'ret': SMC_OLD.replace('\t\t\tgoto fail;\n', '\t\t\t*pr = -1;\n').replace('\t\tbreak;\n\tdefault:', '\t\treturn;\n\tdefault:')}


def tail(kind, lab, exp):
    t = TAIL_OLD
    if not lab:
        t = t.replace('\t\tt5le: __attribute__((hot));\n', '')
    if not exp:
        t = t.replace('__builtin_expect(*pr != 0, 0)', '*pr != 0')
    if kind == 'plain':
        t = '\t\tif (xb.type <= BUILD_DEVGL16)\n\t\t\tbreak;\n'
    return t


def mk(b, sz, smc, tk, lab, exp):
    b = bdrun.sub(b, SIZE_OLD, SIZE[sz], 1)
    b = bdrun.sub(b, SMC_OLD, SMC[smc], 1)
    b = bdrun.sub(b, TAIL_OLD, tail(tk, lab, exp), 1)
    used = sz == 'g' or smc == 'g' or tk == 'g'
    end = END_OLD.replace('\t__asm__ __volatile__("");\n', '')
    if not used:
        end = '}\n'
    return bdrun.sub(b, END_OLD, end, 1)


def mkflag(b, tk, lab, exp, init):
    b = bdrun.sub(b, SIZE_OLD, LOG + '\t\t\tbad = 1;\n\t\t\tbreak;\n', 1)
    b = bdrun.sub(b, SMC_OLD, SMC_OLD.replace('goto fail;', 'bad = 1;'), 1)
    b = bdrun.sub(b, TAIL_OLD, tail(tk, lab, exp).replace('goto fail;', 'bad = 1;'), 1)
    b = bdrun.sub(b, END_OLD, '\tif (bad)\n\t\t*pr = -1;\n}\n', 1)
    i = b.index('static void loadBl(')
    j = b.index('\tint type;\n', i)
    decl = '\tint type;\n\tint bad = 0;\n' if init == 'decl' else '\tint type;\n\tint bad;\n'
    b = b[:j] + decl + b[j + len('\tint type;\n'):]
    if init == 'stmt':
        b = bdrun.sub(b, '\ttype = e->type;\n\tswitch (type) {\n\tcase 5:', '\tbad = 0;\n\ttype = e->type;\n\tswitch (type) {\n\tcase 5:', 1)
    return b


def CASES(base):
    out = []
    for sz, smc, tk in itertools.product(SIZE, SMC, ['g', 'plain']):
        labs = [(1, 1), (0, 1), (1, 0), (0, 0)] if tk == 'g' else [(0, 0)]
        for lab, exp in labs:
            out.append(('%s %s %s%s%s' % (sz, smc, tk, ' lab' if lab else '', ' exp' if exp else ''),
                        lambda b, a=(sz, smc, tk, lab, exp): mk(b, *a)))
    for tk in ['g', 'plain']:
        labs = [(1, 1), (0, 1), (1, 0), (0, 0)] if tk == 'g' else [(0, 0)]
        for (lab, exp), init in itertools.product(labs, ['decl', 'stmt']):
            out.append(('flag %s %s%s%s' % (init, tk, ' lab' if lab else '', ' exp' if exp else ''),
                        lambda b, a=(tk, lab, exp, init): mkflag(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
