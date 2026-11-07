"""Attempt 42, lab_none by two factors at once (attempt 41's lead): case 24's forms in loadConsoleBlFiles (two calls,
`||`, the glitch test folded into the condition, breaks on the keep path, a re-tested r) crossed with the precheck +
cold label kept or gone and with defaultBl60 reached once or twice.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd543.py -n 1000`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd530 import PRECHECK, TAIL

FOCUS = ['_loadConsoleBlFiles']
C24 = '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
FORMS = {
    'src': C24,
    'or': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
    'and_or': '''			case 24:
				if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))
					r = defaultBl60(e);
				break;
''',
    'brk2': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e) && e->size == 0x60)
					break;
				r = defaultBl60(e);
				break;
''',
    'brk_nest': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e)) {
					if (e->size == 0x60)
						break;
				}
				r = defaultBl60(e);
				break;
''',
    'glit_in': '''			case 24:
				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''',
    'glit_in_or': '''			case 24:
				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e) || e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''',
    'r_or': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				r = loadBaseFile(e->name, e);
				if (r || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
    'r_size': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					e->size = 0;
				if (e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
}


def nolab(t):
    t = bdrun.sub(t, PRECHECK, '', 1)
    return bdrun.sub(t, TAIL, '\treturn 0;\n}', 1)


def CASES(base):
    out = []
    for f, txt in FORMS.items():
        for lab in (1, 0):
            out.append(('%s lab%d' % (f, lab), lambda t, txt=txt, lab=lab: (lambda u: u if lab else nolab(u))(bdrun.sub(t, C24, txt, 1))))
    return out
