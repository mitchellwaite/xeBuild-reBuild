"""Attempt 32: lab_none on the plain-`for` base (no precheck, no cold label: 4 loose / 8 strict, only the r = 1 block
and the not-entered return swapped) by defaultBl60's body: result-variable joins (`int r = 1; .. r = 0; return r;`),
success first (nested if), and the console case 24 as `||` or with r.  Runs on src as of ccf9746b."""
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
    'nest': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}''',
    'rvar': '''static int defaultBl60(struct fileent *e)
{
	int r = 1;

	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		r = 0;
	}
	return r;
}''',
    'rvar0': '''static int defaultBl60(struct fileent *e)
{
	int r = 0;

	e->data = malloc(0x60);
	if (!e->data)
		r = 1;
	else {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return r;
}''',
    'rvaru': '''static int defaultBl60(struct fileent *e)
{
	uint32_t r = 1;

	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		r = 0;
	}
	return r;
}''',
    'u32': DEF_OLD.replace('static int defaultBl60', 'static uint32_t defaultBl60'),
    'eq': DEF_OLD.replace('if (!e->data)', 'if (e->data == NULL)'),
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
    return out
