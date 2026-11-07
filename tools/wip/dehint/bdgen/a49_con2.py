"""Attempt 49: console case 24 through a helper that holds its glitch guard (the guard's skip
edge is then an early return), with and without loadBlFiles sharing a helper.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_con2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a49_con import BASE, strip, c24

H = {
 'g1': '''static int loadGlitchBl(struct fileent *e)
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
 'g2': '''static int loadGlitchBl(struct fileent *e)
{
	int r = 0;

	if (xb.glitch2mfg) {
		if (loadBaseFile(e->name, e))
			r = defaultBl60(e);
		else if (e->size != 0x60)
			r = defaultBl60(e);
	}
	return r;
}
''',
 'g3': '''static int loadGlitchBl(struct fileent *e)
{
	if (xb.glitch2mfg) {
		if (loadBaseFile(e->name, e) || e->size != 0x60)
			return defaultBl60(e);
	}
	return 0;
}
''',
 'g4': '''static int loadGlitchBl(struct fileent *e)
{
	if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))
		return defaultBl60(e);
	return 0;
}
''',
}


def mk(h, inl=''):
    def f(t):
        t = strip(t)
        t = t.replace('int loadConsoleBlFiles(void)\n', inl + h + '\nint loadConsoleBlFiles(void)\n', 1)
        return c24(t, '\t\t\t\tr = loadGlitchBl(e);\n\t\t\t\tbreak;\n')
    return f


V = {}
for k, h in H.items():
    V[k] = mk(h)
    V[k + '_ng'] = mk(h.replace('static int', 'int', 1))
