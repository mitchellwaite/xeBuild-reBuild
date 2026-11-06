"""Attempt 3: static helpers around applyIniOptions' xellbutton site, big enough not to be
early-inlined (IPA inlines them, called once), so the site gets its own profile estimate.
On top of optricks part+m_bx with parseButton's winbutton expect also removed (opbtn's noexp:
same 335 as with it).

python tools/wip/dehint/ophelp.py [-o DIR] [names..]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, opbtn

LOG = 'log_printf(1, "default console DVD eject button is being used to start xell\\n");'
XB = '''		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
		}
''' % LOG
XB2 = '''		if (!xb.xellAltButton && (xb.bootFlags & 4)) {
			/* a dead edge into the remopower test: its block keeps a
			   count above its edge's */
			xb.xellAltButton = parseButton(getIniValue("xellbutton2"));
			if (!xb.xellButton)
				log_printf(1, "alternate xell button is disabled\\n");
		}
'''
XB2N = XB2.replace('''			/* a dead edge into the remopower test: its block keeps a
			   count above its edge's */
''', '')


def dedent(s):
    return ''.join(l[1:] if l.startswith('\t') else l for l in s.splitlines(True))


def base():
    return opbtn.build(opbtn.V['noexp'])


def helper(t, defn, call, old):
    assert old in t, old[:60]
    t = t.replace(old, call)
    k = t.index('/* options from perbox files and options.ini')
    return t[:k] + defn + '\n' + t[k:]


V = {}
V['none'] = lambda t: t
V['xb_void'] = lambda t: helper(t, 'static void xellButtonIni(void)\n{\n' + dedent(XB) + '}\n',
                                '\t\txellButtonIni();\n', XB)
V['xb12_void'] = lambda t: helper(t, 'static void xellButtonsIni(void)\n{\n' + dedent(XB) + dedent(XB2N) + '}\n',
                                  '\t\txellButtonsIni();\n', XB + XB2)
# the helper takes the name, both sites use it
GEN = '''static int iniButton(const char *name, int def)
{
	int b = parseButton(getIniValue(name));

	if (!b && def) {
		%s
		b = def;
	}
	return b;
}
''' % LOG
V['xb_s'] = lambda t: helper(t, '''static int xellButtonIni(void)
{
	char *s = getIniValue("xellbutton");
	int b;

	b = parseButton(s);
	if (!b) {
		%s
		b = 0x12;
	}
	return b;
}
''' % LOG, '''		if (!xb.xellButton && (xb.bootFlags & 4))
			xb.xellButton = xellButtonIni();
''', XB)


def jtag(t):
    i = t.index('\tif (xb.type - BUILD_JTAG <= 3) {\n')
    j = t.index('\t/* outside the block above', i)
    blk = t[i:j]
    body = blk[blk.index('{\n') + 2: blk.rindex('\t}\n')]
    defn = 'static void jtagIniOptions(void)\n{\n' + dedent(body) + '}\n'
    t = t[:i] + '\tif (xb.type - BUILD_JTAG <= 3)\n\t\tjtagIniOptions();\n' + t[j:]
    k = t.index('/* options from perbox files and options.ini')
    return t[:k] + defn + '\n' + t[k:]


V['jtag'] = jtag


def run(n):
    return n, optlib.fmt(optlib.score_text(V[n](base())))


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if a[:1] == ['-o']:
        out = a[1]
        a = a[2:]
        os.makedirs(out, exist_ok=True)
    names = a or list(V)
    if out:
        for n in names:
            open(os.path.join(out, n + '.c'), 'w', newline='\n').write(V[n](base()))
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, names):
            print(n, r)
