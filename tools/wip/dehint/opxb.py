"""opxb.py [-o DIR] [names..]: natural forms of applyIniOptions' xellbutton block on top of
optricks part+m_bx (parseButtonX gone, gcc's own parseButton split).  Scores each with optlib;
-o DIR writes each variant's source there (for p1/run.sh dumps)."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

OLD = '''			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\\n");
				xb.xellButton = 0x12;
			}
'''
LOG = 'log_printf(1, "default console DVD eject button is being used to start xell\\n");'
V = {
    'base': OLD,
    'ifs': '''			s = getIniValue("xellbutton");
			if (s)
				xb.xellButton = parseButton(s);
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'ifs_else': '''			s = getIniValue("xellbutton");
			if (s)
				xb.xellButton = parseButton(s);
			else
				xb.xellButton = 0;
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'tern': '''			s = getIniValue("xellbutton");
			xb.xellButton = s ? parseButton(s) : 0;
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'ifs_nest': '''			s = getIniValue("xellbutton");
			if (s)
				xb.xellButton = parseButton(s);
			if (!s || !xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'assign': '''			if (!(xb.xellButton = parseButton(getIniValue("xellbutton")))) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'else': '''			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (xb.xellButton)
				;
			else {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'eq0': '''			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (xb.xellButton == 0) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'iflog': '''			s = getIniValue("xellbutton");
			if (s && (xb.xellButton = parseButton(s)))
				;
			else {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'ifs_if': '''			s = getIniValue("xellbutton");
			if (s)
				xb.xellButton = parseButton(s);
			if (!s) {
				%s
				xb.xellButton = 0x12;
			} else if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % (LOG, LOG),
    'ret12': '''			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (xb.xellButton == 0) {
				%s
				xb.xellButton = 0x12;
			} else
				;
''' % LOG,
    'tern2': '''			s = getIniValue("xellbutton");
			xb.xellButton = s ? parseButton(s) : 0;
			if (xb.xellButton == 0) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'ifelse_s': '''			s = getIniValue("xellbutton");
			if (!s)
				xb.xellButton = 0;
			else
				xb.xellButton = parseButton(s);
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'tern_not': '''			s = getIniValue("xellbutton");
			xb.xellButton = !s ? 0 : parseButton(s);
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'and': '''			s = getIniValue("xellbutton");
			if (!s || !(xb.xellButton = parseButton(s))) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
    'nest': '''			s = getIniValue("xellbutton");
			xb.xellButton = parseButton(s);
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG,
}


# wrappers: (helper defined before applyIniOptions, xellbutton block, other sites use helper?)
W = {
    'w_ini': ('''static int iniButton(const char *name)
{
	return parseButton(getIniValue(name));
}

''', '''			xb.xellButton = iniButton("xellbutton");
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG, False),
    'w_ini_all': ('''static int iniButton(const char *name)
{
	return parseButton(getIniValue(name));
}

''', '''			xb.xellButton = iniButton("xellbutton");
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG, True),
    'w_def': ('''static int xellButtonIni(void)
{
	int b = parseButton(getIniValue("xellbutton"));

	if (!b) {
		%s
		b = 0x12;
	}
	return b;
}

''' % LOG.replace('\\n', '\\n'), '''			xb.xellButton = xellButtonIni();
''', False),
    'w_void': ('''static void xellButtonIni(void)
{
	xb.xellButton = parseButton(getIniValue("xellbutton"));
	if (!xb.xellButton) {
		%s
		xb.xellButton = 0x12;
	}
}

''' % LOG, '''			xellButtonIni();
''', False),
    'w_s': ('''static int iniButton(const char *name)
{
	const char *s = getIniValue(name);

	if (!s)
		return 0;
	return parseButton(s);
}

''', '''			xb.xellButton = iniButton("xellbutton");
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG, False),
    'w_s_all': ('''static int iniButton(const char *name)
{
	const char *s = getIniValue(name);

	if (!s)
		return 0;
	return parseButton(s);
}

''', '''			xb.xellButton = iniButton("xellbutton");
			if (!xb.xellButton) {
				%s
				xb.xellButton = 0x12;
			}
''' % LOG, True),
}


def make(name):
    t, got = optricks.apply(optricks.base(), ['part', 'm_bx'])
    assert got == ['part', 'm_bx'], got
    assert OLD in t
    if name in W:
        helper, blk, allsites = W[name]
        t = t.replace(OLD, blk)
        if allsites:
            t = t.replace('parseButton(getIniValue("xellbutton2"))', 'iniButton("xellbutton2")')
            t = t.replace('parseButton(getIniValue("dualboot"))', 'iniButton("dualboot")')
        i = t.index('void applyIniOptions(void)\n{')
        i = t.rindex('\n\n', 0, i) + 2
        # before applyIniOptions' leading comment, if any
        return t[:i] + helper + t[i:]
    return t.replace(OLD, V[name])


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
        os.makedirs(out, exist_ok=True)
    names = a or list(V) + list(W)

    def one(n):
        t = make(n)
        if out:
            open(os.path.join(out, n + '.c'), 'w', newline='\n').write(t)
        return n, optlib.score_text(t)
    with ThreadPoolExecutor(6) as p:
        for n, r in p.map(one, names):
            print('%-10s %s' % (n, optlib.fmt(r)), flush=True)
