"""Attempt 21: the SE path with its own checkBl and kit test (the path vrp2 copies X for, written out), so its `<=5`
test gets its own profile_estimate probability (early return against `<=5` and PRED_CALL against the setFlashBuild side)
instead of inheriting the joiner copy's.  Same behaviour: for type 14 the shared code after chk: only breaks on a
failed check and calls setFlashBuild on a kit build.  t5le / the `*pr` expect on or off."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
		}
'''
S = 'setFlashBuild(getBeU16(xb.files[i].data + 2));'
SE = {
    'brk': '''			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
			*pr = checkBl(e->data, e->size, @T@, e->crc);
			if (*pr)
				break;
			if (xb.type > BUILD_DEVGL16)
				@S@
			break;
		}
''',
    'and': '''			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
			*pr = checkBl(e->data, e->size, @T@, e->crc);
			if (!*pr && xb.type > BUILD_DEVGL16)
				@S@
			break;
		}
''',
    'le': '''			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
			*pr = checkBl(e->data, e->size, @T@, e->crc);
			if (*pr || xb.type <= BUILD_DEVGL16)
				break;
			@S@
			break;
		}
''',
}
TY = {'14': '14', 'type': 'type'}
HS = [(), ('lab_t5le',), ('exp_pr',), ('lab_t5le', 'exp_pr')]


def mk(b, se, ty, hs):
    t = bdrun.sub(b, OLD, SE[se].replace('@T@', TY[ty]).replace('@S@', S))
    return bdhints.off(t, *hs) if hs else t


def CASES(base):
    out = []
    for se, ty, hs in itertools.product(SE, TY, HS):
        out.append(('%s %s -%s' % (se, ty, ','.join(hs)), lambda b, c=(se, ty, hs): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
