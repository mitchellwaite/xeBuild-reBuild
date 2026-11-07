"""Attempt 30: whole-structure axes for loadBl with all seven loadBl hints off (a30lib.off7), scored together.
Axes:
  RES   ptr: src's `*pr`; retu / reti: a local `uint32_t r` / `int r` returned (`static uint32_t|int loadBl(e, i)`,
        caller `r = loadBl(e, i);`); loc: a local stored once (`*pr = r;` at the end).
  FB    src's if/else-if fallback, and9 (attempt 25).
  FAIL  end (src's label after the switch), c2 (closing case 2, attempt 26), ret (ret forms only: `return -1;` at
        each failure site, no label).
  SIG   src (`if (pub1bl) { if (!verify) fail; else passed } else nokey`), srcp (verify tested positively), nk (no key
        first: `if (!pub1bl) nokey; else if (!verify) fail; else passed`), nkp (no key first, verify positive).
  TAIL  src (`if (xb.type <= 5) { if (r) ERR; break; }`), plain (`if (xb.type <= 5) break;`), and
        (`if (xb.type > 5 && type == 14)`).
Behaviour: every form returns/stores the same r on every path (the src tail's `if (r) ERR` re-sets -1 where r is
already -1)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from a30lib import off7, LB, LBF, setfn

FB_SRC = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
FB_AND9 = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (type == 10 && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
SIGTAIL = '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				} else
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
			} else
				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
		}
		/* the expect leaves vrp1's signature-failed copy of this test a
		   >5 edge (else its setFlashBuild copy has frequency 0 and final
		   aligns the type-11 block after it); the hot label keeps the SE
		   copy's <=5 edge the likely one (jbe) */
		if (xb.type <= BUILD_DEVGL16) {
			if (*pr != 0)
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
FAILED = '''log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;'''
PASSED = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);'
NOKEY = 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);'
SIG = {
    'src': '''			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					%s
				} else
					%s
			} else
				%s
''' % (FAILED, PASSED, NOKEY),
    'srcp': '''			if (xb.pub1bl) {
				if (cbVerifySig(e->data, xb.pub1bl))
					%s
				else {
					%s
				}
			} else
				%s
''' % (PASSED, FAILED, NOKEY),
    'nk': '''			if (!xb.pub1bl)
				%s
			else if (!cbVerifySig(e->data, xb.pub1bl)) {
				%s
			} else
				%s
''' % (NOKEY, FAILED.replace('\t\t\t\t\t', '\t\t\t\t'), PASSED),
    'nkp': '''			if (!xb.pub1bl)
				%s
			else if (cbVerifySig(e->data, xb.pub1bl))
				%s
			else {
				%s
			}
''' % (NOKEY, PASSED, FAILED.replace('\t\t\t\t\t', '\t\t\t\t')),
}
TAIL = {
    'src': '''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr != 0)
				ERR;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
    'plain': '''		if (xb.type <= BUILD_DEVGL16)
			break;
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
    'and': '''		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
}
C2A = '''		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			goto fail;
		break;
'''
C2B = '''		e->offset = smcSetLoad(e->size);
		if (e->offset)
			break;
	fail:
		*pr = -1;
		break;
'''
ENDA = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	*pr = -1;
}
'''
ENDF = '\treturn;\nfail:\n\t*pr = -1;\n}\n'
LOOP_CALL = '''		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
'''


def mk(b, res, fb, fail, sig, tail):
    if fail == 'ret' and res not in ('retu', 'reti'):
        return None
    i, j = bdrun.fnspan(b, LB)
    f = b[i:j]
    f = bdrun.sub(f, ENDA, ENDF, 1)
    if fb == 'and9':
        f = bdrun.sub(f, FB_SRC, FB_AND9, 1)
    f = bdrun.sub(f, SIGTAIL, '''		if (type == 5 || type == 17 || type == 11) {
%s		}
''' % SIG[sig] + TAIL[tail], 1)
    err = 'return -1' if fail == 'ret' else 'goto fail'
    f = f.replace('ERR;', err + ';')
    if fail == 'c2':
        f = bdrun.sub(f, C2A, C2B, 1)
        f = bdrun.sub(f, ENDF, '}\n', 1)
    elif fail == 'ret':
        f = bdrun.sub(f, C2A, C2A.replace('goto fail', 'return -1'), 1)
        f = bdrun.sub(f, '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;''', '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			return -1;''', 1)
        f = bdrun.sub(f, ENDF, '}\n', 1)
    if res in ('retu', 'reti', 'loc'):
        k = f.index('{')
        f = f[:k] + f[k:].replace('*pr', 'r')
        if res == 'loc':
            f = bdrun.sub(f, '{\n\tint type;\n', '{\n\tuint32_t r = 0;\n\tint type;\n', 1)
            if fail == 'end':
                f = bdrun.sub(f, '\treturn;\nfail:\n\tr = -1;\n}\n', '\t*pr = r;\n\treturn;\nfail:\n\t*pr = -1;\n}\n', 1)
            else:
                f = bdrun.sub(f, '\t}\n}\n', '\t}\n\t*pr = r;\n}\n', 1)
        else:
            t = 'uint32_t' if res == 'retu' else 'int'
            f = bdrun.sub(f, 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n',
                          'static %s loadBl(struct fileent *e, uint32_t i)\n{\n\t%s r = 0;\n\tint type;\n' % (t, t), 1)
            if fail == 'end':
                f = bdrun.sub(f, '\treturn;\nfail:\n\tr = -1;\n}\n', '\treturn r;\nfail:\n\treturn -1;\n}\n', 1)
            else:
                f = bdrun.sub(f, '\t}\n}\n', '\t}\n\treturn r;\n}\n', 1)
    b = b[:i] + f + b[j:]
    if res in ('retu', 'reti'):
        b = bdrun.sub(b, LOOP_CALL, LOOP_CALL.replace('loadBl(e, i, &r);', 'r = loadBl(e, i);'), 1)
    return b


RES = ['ptr', 'retu', 'reti', 'loc']
FBS = ['src', 'and9']
FAILS = ['end', 'c2', 'ret']
SIGS = list(SIG)
TAILS = list(TAIL)


def PRE(b):
    return off7(b)


def CASES(base):
    return [(' '.join(k), lambda b, k=k: mk(b, *k)) for k in itertools.product(RES, FBS, FAILS, SIGS, TAILS)]


FOCUS = ['_loadBlFiles']
