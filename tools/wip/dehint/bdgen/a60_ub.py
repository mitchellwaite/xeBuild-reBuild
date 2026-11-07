"""Attempt 60: a60_est.py's `ub` (useBuiltIn for cases 1 / 22, memmove) frees lab_devgl's layout but its
r = 1 block (115 > freq_max / 100 = 95) gets a loop alignment.  Helper forms and sites, all with the
devgl label off.  python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a60_ub.py [-o ..]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a60_est import UB_FN, ub_case, BL60
LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
HD = '/* the default 0x60-byte bootloader (type 24).'
C1 = ub_case('payload', 'defPayload', 0x200)
C22 = ub_case('core', 'defCore', 0xd40)
BODY = '''	e->data = malloc(size);
	if (!e->data)
		return 1;
	e->size = size;
	memmove(e->data, data, size);
	return 0;
'''
FORMS = {
    'p': BODY,
    'nest': '''	e->data = malloc(size);
	if (e->data) {
		e->size = size;
		memmove(e->data, data, size);
		return 0;
	}
	return 1;
''',
    'r': '''	int r = 1;

	e->data = malloc(size);
	if (e->data) {
		e->size = size;
		memmove(e->data, data, size);
		r = 0;
	}
	return r;
''',
    'asg': BODY.replace('\te->data = malloc(size);\n\tif (!e->data)\n', '\tif (!(e->data = malloc(size)))\n'),
    'loc': '''	uint8_t *p = malloc(size);

	e->data = p;
	if (!p)
		return 1;
	e->size = size;
	memmove(p, data, size);
	return 0;
''',
    'mc': BODY.replace('memmove', 'memcpy'),
}
SIGS = {
    '': None,
    'u': ('static int useBuiltIn', 'static uint32_t useBuiltIn'),
    'z': ('const uint8_t *data, uint32_t size)', 'const void *data, size_t size)'),
    'i': ('const uint8_t *data, uint32_t size)', 'const uint8_t *data, int size)'),
}
V = {}
for fk, body in FORMS.items():
    for sk, sg in SIGS.items():
        fn = UB_FN.replace(BODY, body)
        if sg:
            fn = fn.replace(*sg)
        for site, cs in (('12', [C1, C22]), ('1', [C1]), ('22', [C22]), ('12b', [C1, C22, (BL60, '\treturn useBuiltIn(e, defBl60, 0x60);\n')]),
                         ('b', [(BL60, '\treturn useBuiltIn(e, defBl60, 0x60);\n')])):
            V['%s%s_%s' % (fk, sk, site)] = [LAB, (HD, fn + HD)] + cs
SETS = {k: ['-'] for k in V}
