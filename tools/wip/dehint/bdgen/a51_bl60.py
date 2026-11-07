"""Attempt 51: defaultBl60's own NULL-edge probability (10.1% in src: pointer 15% with the early
return's 39%) is the other factor of console's r = 1 block (case 24 call x loadBl24's share x this).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_bl60.py [-p 95,99]
A51_OFF picks the hint sets (default all,none)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub

BASE = H.BASE
OLD = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}
'''
BODIES = {
    'if': '''	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}
''',
    'r': '''	int r = 1;

	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		r = 0;
	}
	return r;
}
''',
    'r0': '''	int r = 0;

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
    'else': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	else {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}
''',
    'ret': '''	e->data = malloc(0x60);
	if (e->data == NULL)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}
''',
    'bool': '''	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return e->data == NULL;
}
''',
}
OFF = {'all': [], 'none': [H.NONE, H.NONE2]}
V = {}
for b, body in BODIES.items():
    for k in os.environ.get('A51_OFF', 'all,none').split(','):
        def f(t, body=body, p=OFF[k]):
            t = sub(t, OLD, body)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V['%s_%s' % (b, k)] = f
