"""Attempt 50: loadBl24's body (both loaders call it), with the hints off one at a time.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_bl24.py [-p 95,99]
Its early returns keep their PRED_TREE_EARLY_RETURN through early inlining (attempt 50's reading),
so the body's form sets the defaultBl60 call blocks' frequencies in both callers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF

BASE = H.BASE
OLD = '''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}
'''
BODIES = {
    'src': OLD,
    'or': '''	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;
}
''',
    'and': '''	if (!loadBaseFile(e->name, e) && e->size == 0x60)
		return 0;
	return defaultBl60(e);
}
''',
    'r2': '''	int r = 0;

	if (loadBaseFile(e->name, e))
		r = defaultBl60(e);
	else if (e->size != 0x60)
		r = defaultBl60(e);
	return r;
}
''',
    'nest': '''	if (!loadBaseFile(e->name, e)) {
		if (e->size == 0x60)
			return 0;
	}
	return defaultBl60(e);
}
''',
    'ok1': '''	if (!loadBaseFile(e->name, e)) {
		if (e->size == 0x60)
			return 0;
		return defaultBl60(e);
	}
	return defaultBl60(e);
}
''',
    'g0': '''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size == 0x60)
		return 0;
	return defaultBl60(e);
}
''',
    'n2': '''	if (!loadBaseFile(e->name, e)) {
		if (e->size != 0x60)
			return defaultBl60(e);
		return 0;
	}
	return defaultBl60(e);
}
''',
    'n3': '''	if (!loadBaseFile(e->name, e)) {
		if (e->size == 0x60)
			return 0;
	} else
		return defaultBl60(e);
	return defaultBl60(e);
}
''',
    'r3': '''	int r = 0;

	if (loadBaseFile(e->name, e))
		r = defaultBl60(e);
	else if (e->size != 0x60)
		r = defaultBl60(e);
	else
		return 0;
	return r;
}
''',
    'r4': '''	int r;

	if (loadBaseFile(e->name, e))
		r = defaultBl60(e);
	else if (e->size != 0x60)
		r = defaultBl60(e);
	else
		r = 0;
	return r;
}
''',
    'r5': '''	if (!loadBaseFile(e->name, e)) {
		if (e->size == 0x60)
			return 0;
		return defaultBl60(e);
	}
	return defaultBl60(e);
}
''',
    'r6': '''	if (loadBaseFile(e->name, e) == 0 && e->size == 0x60)
		return 0;
	if (loadBaseFile == 0)
		return 0;
	return defaultBl60(e);
}
''',
    'sz': '''	if (!loadBaseFile(e->name, e) && e->size == 0x60)
		return 0;
	if (e->data)
		free(e->data);
	return defaultBl60(e);
}
''',
}
NONEL = ('none: __attribute__((cold));\n\treturn 0;\n', '')
V = {}
for b, body in BODIES.items():
    if b in ('sz', 'r6'):
        continue  # frees e->data: a behaviour change, kept only as a note
    for k in os.environ.get('A50_OFF', 'all,pr,lab,none').split(','):
        def f(t, body=body, p=OFF[k]):
            t = sub(t, OLD, body)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V['%s_%s' % (b, k)] = f
