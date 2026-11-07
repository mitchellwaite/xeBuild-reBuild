"""Attempt 33: lab_none by defaultBl60's *return value* rather than its spelling (gen_bd281 / gen_bd443 only tried forms
that return constants, which all get PRED_CONST_RETURN against the malloc-failed path, directly or through the PHI).
Here the result is computed: `return e->data == NULL;`, `return !e->data;`, a size check `return e->size != 0x60`,
so the return predictor has no constant to act on and the r = 1 block (14 against the not-entered return's 20 on the
plain-`for` base) may get another frequency.  Each on src (precheck and cold label kept) and on the plain-`for` base.
Runs on src as of 5a0bc459."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun

FOCUS = ['_loadConsoleBlFiles', '_loadBlFiles']

DEF_OLD = '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}'''
DEFS = {
    'src': DEF_OLD,
    'eqnull': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return e->data == NULL;
}''',
    'not': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return !e->data;
}''',
    'size': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return e->data ? 0 : 1;
}''',
    'local': '''static int defaultBl60(struct fileent *e)
{
	uint8_t *p = malloc(0x60);

	e->data = p;
	if (p) {
		e->size = 0x60;
		memcpy(p, defBl60, 0x60);
	}
	return p == NULL;
}''',
}

PRE_OLD = '''	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1;'''
LAB_OLD = '''	return 0;
none: __attribute__((cold));
	return 0;
}'''


def CASES(base):
    out = []
    for k, d in DEFS.items():
        t = bdrun.sub(base, DEF_OLD, d, 1)
        out.append((k + ' label', t))
        t2 = bdrun.sub(bdrun.sub(t, PRE_OLD, '	for (i = 1;'), LAB_OLD, '	return 0;\n}')
        out.append((k + ' plain', t2))
        out.append((k + ' nocold', t.replace('none: __attribute__((cold));', 'none:')))
    return out
