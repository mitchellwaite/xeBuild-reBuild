"""Attempt 41, lab_none: raise the switch's share of loadConsoleBlFiles' loop body (and so the r = 1 block, case 24's
defaultBl60 malloc failure) without touching the not-entered return: the none test as a `continue` (PRED_CONTINUE on
the skip edge, so the switch gets more than the `||`'s 75%), crossed with case 24's two-call and `||` forms, the
precheck + label kept or gone (plain `for`), and loadBlFiles spelled the same or not.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd530.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FOCUS = ['_loadConsoleBlFiles', '_loadBlFiles']
PRECHECK = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
TAIL = '''	return 0;
none: __attribute__((cold));
	return 0;
}'''
NONE_C = '''		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;
'''
NONE_FORMS = {
    'src': NONE_C,
    'cont': '''		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		{
			int type = e->type;
''',
    'cont_eq': '''		if (strnicmp(e->name, "none", 4) == 0 && e->crc == 0)
			continue;
		{
			int type = e->type;
''',
    'cont_nest': '''		if (!strnicmp(e->name, "none", 4)) {
			if (!e->crc)
				continue;
		}
		{
			int type = e->type;
''',
}
C24 = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
C24_FORMS = {
    'two': C24,
    'or': '''				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
}
LB = '''		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
'''
LB_CONT = '''		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		loadBl(e, i, &r);
'''


def CASES(base):
    out = []
    for pk in ('plain', 'label'):
        for nk, nv in NONE_FORMS.items():
            for ck, cv in C24_FORMS.items():
                for lk in ('lb', 'lbc'):
                    if lk == 'lbc' and nk == 'src':
                        continue
                    def f(b, pk=pk, nv=nv, cv=cv, lk=lk):
                        if pk == 'plain':
                            b = bdrun.sub(b, PRECHECK, '', 1)
                            b = bdrun.sub(b, TAIL, '\treturn 0;\n}', 1)
                        b = bdrun.sub(b, NONE_C, nv, 1)
                        b = bdrun.sub(b, C24, cv, 1)
                        if lk == 'lbc':
                            b = bdrun.sub(b, LB, LB_CONT, 1)
                        return b
                    out.append(('%s %s %s %s' % (pk, nk, ck, lk), f))
    return out
