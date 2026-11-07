"""Attempt 55: lab_devgl.  The r = 1 block (bbro's trace after arm 1's retest) must be laid out before
the suGetCF block: it needs freq >= 42 (round 4, ahead of the suGetCF block's 41) or >= 44.1
(round 3); without the label it is 37 (arm 2's malloc failure 5 + cases 1 / 22's malloc failures
14 + 14 + the retest's fall-through ~0).  Rows try to raise its sources naturally.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a55_dev.py [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE

LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')


def case(n, what, name, size):
    return ('\t\t\t\tlog_printf(1, "could not read %%s%%s, using built in %s (0x%%x bytes)\\n", xb.binDir, e->name, 0x%x);\n'
            '\t\t\t\te->data = malloc(0x%x);\n\t\t\t\tif (!e->data) {\n\t\t\t\t\tr = 1;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n'
            '\t\t\t\te->size = 0x%x;\n\t\t\t\tmemcpy(e->data, %s, 0x%x);\n\t\t\t\tbreak;\n') % (what, size, size, size, name, size)


def case_new(what, name, size, call):
    return ('\t\t\t\tlog_printf(1, "could not read %%s%%s, using built in %s (0x%%x bytes)\\n", xb.binDir, e->name, 0x%x);\n'
            '\t\t\t\tr = %s(e, %s, 0x%x);\n\t\t\t\tbreak;\n') % (what, size, call, name, size)


C1 = case(1, 'payload', 'defPayload', 0x200)
C22 = case(22, 'core', 'defCore', 0xd40)

BL60 = '''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}
'''
HELP = '''/* a built-in copy in place of a file that couldn't be read */
static int useBuiltIn(struct fileent *e, const uint8_t *data, uint32_t size)
{
	e->data = malloc(size);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
}

'''
HELP_V = HELP.replace('static int useBuiltIn', 'static uint32_t useBuiltIn')


def mk(call=True, bl60=False, lab=False, helper=HELP, c1=True, c22=True):
    ed = []
    if not lab:
        ed.append(LAB)
    if call:
        if bl60:
            ed.append((BL60, helper + 'static int defaultBl60(struct fileent *e)\n{\n\treturn useBuiltIn(e, defBl60, 0x60);\n}\n'))
        else:
            ed.append(('/* the default 0x60-byte bootloader (type 24) */\n', helper + '/* the default 0x60-byte bootloader (type 24) */\n'))
        if c1:
            ed.append((C1, case_new('payload', 'defPayload', 0x200, 'useBuiltIn')))
        if c22:
            ed.append((C22, case_new('core', 'defCore', 0xd40, 'useBuiltIn')))
    return ed


V = {
    'lab_src': [],
    'nolab': mk(call=False),
    'h12': mk(), 'h12_L': mk(lab=True),
    'h1': mk(c22=False), 'h22': mk(c1=False),
    'h12b': mk(bl60=True), 'h12b_L': mk(bl60=True, lab=True),
    'h12u': mk(helper=HELP_V),
}
