"""Attempt 51: with loadBl24's one-call `||` body, console's precheck and cold label are free except
for the size store's place (sched2 puts `mov [ebx+4],0x60` after the copy's register setup).
defaultBl60 forms that might keep the store first, on the `or` body with loadBlFiles' second arm
calling loadBl24 (or written out), devgl label on.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_store.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, LAB
import a50_bl24 as B
import a50_arm2 as A
import a51_bl60 as D

BASE = H.BASE
F = {
    'src': D.OLD,
    'cpy1': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	memcpy(e->data, defBl60, 0x60);
	e->size = 0x60;
	return 0;
}
''',
    'ptr': '''	uint8_t *p;

	e->data = p = malloc(0x60);
	if (!p)
		return 1;
	e->size = 0x60;
	memcpy(p, defBl60, 0x60);
	return 0;
}
''',
    'ptr2': '''	uint8_t *p = malloc(0x60);

	e->data = p;
	if (!p)
		return 1;
	e->size = 0x60;
	memcpy(p, defBl60, 0x60);
	return 0;
}
''',
    'sz': '''	e->data = malloc(sizeof(defBl60));
	if (!e->data)
		return 1;
	e->size = sizeof(defBl60);
	memcpy(e->data, defBl60, sizeof(defBl60));
	return 0;
}
''',
    'szr': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, e->size);
	return 0;
}
''',
}
V = {}
for b in os.environ.get('A51_B', 'or').split(','):
    for fk, fb in F.items():
        for form in ('w', 'call'):
            for none in (0, 1):
                def g(t, b=b, fb=fb, form=form, none=none):
                    t = sub(t, B.OLD, B.BODIES[b])
                    t = sub(t, D.OLD, fb)
                    if form == 'call':
                        t = A.arm('call', 1)(t)
                    if none:
                        t = sub(t, *H.NONE)
                        t = sub(t, *H.NONE2)
                    return t
                V['%s_%s_%s_%s' % (b, fk, form, 'N' if none else 'k')] = g
