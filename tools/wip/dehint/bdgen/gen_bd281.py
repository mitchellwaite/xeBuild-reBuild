"""Attempt 17, lab_none: with the precheck and cold label gone (a plain `for`), only two round-4 blocks are swapped:
the not-entered `return 0` [20] and the inlined defaultBl60's `r = 1` [14] (malloc failed); round 4 orders them by
frequency.  defaultBl60's own profile sets the 14: `if (!e->data) return 1;` gets the pointer heuristic (NULL
unlikely) and the early return against the failure.  Written the other way round (the success arm returns early)
the early return would count against success instead, which should lift `r = 1` above 20 while staying under
round 3's 44.  Axes: defaultBl60's form x lab_none (label and precheck) on or off.  Runs on src as of d09240ad."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}
'''
FORMS = {
    'src': OLD,
    'pos': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}
''',
    'posr': '''static int defaultBl60(struct fileent *e)
{
	int r = 1;

	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		r = 0;
	}
	return r;
}
''',
    'negr': '''static int defaultBl60(struct fileent *e)
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
}
''',
    'pose': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	} else
		return 1;
	return 0;
}
''',
    'posnull': '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data != NULL) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}
''',
}

NONE_PRE = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
NONE_TAIL = '''	return 0;
none: __attribute__((cold));
	return 0;
}'''


def mk(b, f, none):
    b = bdrun.sub(b, OLD, FORMS[f], 1)
    if not none:
        b = bdrun.sub(b, NONE_PRE, '', 1)
        b = bdrun.sub(b, NONE_TAIL, '\treturn 0;\n}', 1)
    return b


def CASES(base):
    return [('%s none%d' % (f, n), lambda b, f=f, n=n: mk(b, f, n)) for f, n in itertools.product(FORMS, (1, 0))]
