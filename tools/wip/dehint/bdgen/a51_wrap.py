"""Attempt 51: console's case 24 through a wrapper around loadBl24 that holds the glitch guard, so the
guard's skip edge is an early return in the wrapper's own profile (ds(call 29%, early return 61%) =
39% instead of 29%): console's malloc block 716 x 39% x 70% = 195 >= 176 (a51 bbro reading).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_wrap.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub

BASE = H.BASE
OLD = '''				if (xb.glitch2mfg)
					r = loadBl24(e);
				break;
			case 25:'''
NEW = '''				r = loadGlitchBl24(e);
				break;
			case 25:'''
ANCH = '/* load the input files by their type; the arms only set r, which is\n'
W = {
    'w1': '''static int loadGlitchBl24(struct fileent *e)
{
	if (!xb.glitch2mfg)
		return 0;
	return loadBl24(e);
}

''',
    'w2': '''static int loadGlitchBl24(struct fileent *e)
{
	if (xb.glitch2mfg)
		return loadBl24(e);
	return 0;
}

''',
    'w3': '''static int loadGlitchBl24(struct fileent *e)
{
	int r = 0;

	if (xb.glitch2mfg)
		r = loadBl24(e);
	return r;
}

''',
    'w4': '''static int loadGlitchBl24(struct fileent *e)
{
	if (!xb.glitch2mfg)
		return 0;
	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}

''',
    'w5': '''static int loadGlitchBl24(struct fileent *e)
{
	if (!xb.glitch2mfg)
		return 0;
	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size == 0x60)
		return 0;
	return defaultBl60(e);
}

''',
}
V = {}
for w, body in W.items():
    for pos in ('a', 'b'):
        for none in (0, 1):
            def f(t, body=body, none=none, pos=pos):
                if pos == 'a':
                    t = sub(t, ANCH, body + ANCH)
                else:
                    t = sub(t, 'int loadConsoleBlFiles(void)\n', body + 'int loadConsoleBlFiles(void)\n')
                t = sub(t, OLD, NEW)
                if none:
                    t = sub(t, *H.NONE)
                    t = sub(t, *H.NONE2)
                return t
            V['%s%s_%s' % (w, pos, 'N' if none else 'k')] = f
