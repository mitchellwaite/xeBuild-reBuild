"""Attempt 21, loadBl's tail with the kit test first (attempt 11's 4-loose form, no t5le).  Read from dom2: there the
sig-failed path's FSM thread to loadBlFiles' `if (r)` goes through type == 14's false edge (23, 104), not through the
setFlashBuild block (23, 24) (24, 104) as in src, because the join's PHI lists the false edge first; so dom2 copies
the type == 14 test for that path but not setFlashBuild, which dom3 copies after ivopts (the IV read).  Axes: spellings
of the kit arm that change the order of the join's incoming edges, x the `*pr` arm (with or without its expect)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
S = 'setFlashBuild(getBeU16(xb.files[i].data + 2));'
G = 'xb.type > BUILD_DEVGL16'
KIT = {
    # kit arm ends in break; the *pr arm follows
    'k1': '''		if (@G@) {
			if (type == 14)
				@S@
			break;
		}
''',
    'k2': '''		if (@G@) {
			if (type == 14) {
				@S@
				break;
			}
			break;
		}
''',
    'k3': '''		if (@G@) {
			if (type != 14)
				break;
			@S@
			break;
		}
''',
    'k4': '''		if (@G@) {
			if (type == 14)
				@S@
			return;
		}
''',
    'k5': '''		if (@G@) {
			if (type != 14)
				return;
			@S@
			return;
		}
''',
    'k6': '''		if (@G@) {
			if (type == 14) {
				@S@
			}
			break;
		}
''',
    'k7': '''		if (@G@) {
			if (type == 14)
				@S@
			else
				break;
			break;
		}
''',
    'k8': '''		if (@G@) {
			if (type == 14)
				@S@
			goto out;
		}
''',
}
PR = {
    'exp': '''		if (__builtin_expect(*pr != 0, 0))
			goto fail;
		break;
''',
    'pl': '''		if (*pr)
			goto fail;
		break;
''',
    'm1': '''		if (*pr == -1)
			goto fail;
		break;
''',
}
# else forms: the *pr test in the kit test's else
ELSE = {
    'e1': '''		if (@G@) {
			if (type == 14)
				@S@
		} else if (@PR@)
			goto fail;
		break;
''',
    'e2': '''		if (@G@) {
			if (type != 14)
				break;
			@S@
		} else if (@PR@)
			goto fail;
		break;
''',
    'e3': '''		if (!(@G@)) {
			if (@PR@)
				goto fail;
		} else if (type == 14)
			@S@
		break;
''',
}
PRX = {'exp': '__builtin_expect(*pr != 0, 0)', 'pl': '*pr', 'm1': '*pr == -1'}


def mk(b, k, p):
    if k in KIT:
        f = KIT[k] + PR[p]
    else:
        f = ELSE[k].replace('@PR@', PRX[p])
    f = f.replace('@G@', G).replace('@S@', S)
    t = bdrun.sub(b, TAIL, f, 1)
    if k == 'k8':
        t = bdrun.sub(t, '''	return;
	/* one -1 block''', '''out:
	return;
	/* one -1 block''')
    return t


def CASES(base):
    out = []
    for k, p in itertools.product(list(KIT) + list(ELSE), PR):
        out.append(('%s %s' % (k, p), lambda b, c=(k, p): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
