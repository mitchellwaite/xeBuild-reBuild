"""Attempt 35, lab_none by attempt 34's lever: loadConsoleBlFiles' case 24 with the load's result kept in r and
re-tested (flow that vrp1 threads away later), so the r = 1 path (defaultBl60's malloc failure) gets more frequency at
profile_estimate.  Attempt 22's gen_bd331 had `||` (18 of the 21 needed).  lab_none off."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FOCUS = ['_loadConsoleBlFiles']
OLD = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
FORMS = {
    'src': OLD,
    'r_or': '''				r = loadBaseFile(e->name, e);
				if (r || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
    'r_two': '''				r = loadBaseFile(e->name, e);
				if (r)
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
    'r_seq': '''				r = loadBaseFile(e->name, e);
				if (!r && e->size != 0x60)
					r = 1;
				if (r)
					r = defaultBl60(e);
				break;
''',
    'r_seq2': '''				r = loadBaseFile(e->name, e);
				if (!r && e->size != 0x60)
					r = defaultBl60(e);
				else if (r)
					r = defaultBl60(e);
				break;
''',
    'r_retest': '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				if (r)
					break;
				break;
''',
}


def CASES(base):
    out = []
    for k, v in FORMS.items():
        out.append((k, (lambda b, v=v: bdrun.sub(bdhints.off(b, 'lab_none'), OLD, v, 1))))
        out.append((k + '+none', (lambda b, v=v: bdrun.sub(b, OLD, v, 1))))
    return out
