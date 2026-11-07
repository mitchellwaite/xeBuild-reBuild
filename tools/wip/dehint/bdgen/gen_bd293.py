"""Attempt 18, lab_none: the r = 1 block against the not-entered return in round 4.

Attempt 17 took defaultBl60 for early inlined; it isn't: loadConsoleBlFiles calls defaultBl60.isra.0 at
profile_estimate and IPA inlines it late, so its own profile (NULL test: pointer 15% with early return 39% ->
10.1%) is what reaches r = 1 (14 against the return's 20).  Axes: defaultBl60's form (forms whose NULL edge doesn't
go straight to the return block, so no early-return prediction), case 24's form in loadConsoleBlFiles (two calls,
`||`, nested), precheck and label gone.  Runs on src as of 8b56de61."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

PRE_OLD = '\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n'
END_OLD = '\treturn 0;\nnone: __attribute__((cold));\n\treturn 0;\n}'
DB_OLD = '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}'''
DB = {
    'src': DB_OLD,
    'pos': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}''',
    'r': '''static int defaultBl60(struct fileent *e)
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
    'r0': '''static int defaultBl60(struct fileent *e)
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
    'else': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	else {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}''',
    'tern': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return e->data == NULL;
}''',
    'bool': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return !e->data;
}''',
}
C24_OLD = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
			case 25:'''
C24 = {
    'two': C24_OLD,
    'or': '''				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
			case 25:''',
}


def mk(b, db, c24, pre):
    b = bdrun.sub(b, DB_OLD, DB[db], 1)
    b = bdrun.sub(b, C24_OLD, C24[c24], 1)
    if pre == 'none':
        b = bdrun.sub(b, PRE_OLD, '', 1)
        b = bdrun.sub(b, END_OLD, '\treturn 0;\n}', 1)
    return b


def CASES(base):
    out = []
    for db, c24, pre in itertools.product(DB, C24, ['none', 'keep']):
        if db == 'src' and c24 == 'two' and pre == 'keep':
            continue
        out.append(('%s %s %s' % (db, c24, pre), lambda b, c=(db, c24, pre): mk(b, *c)))
    return out


FOCUS = ['_loadConsoleBlFiles', '_loadBlFiles']
