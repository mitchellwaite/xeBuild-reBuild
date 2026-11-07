"""Attempt 16: the natural parseButton split base on today's source.

Removes the hand-written _parseButton.part.0 (cold, section, asm label), parseButton's
winbutton expect, and parseButtonX (its power expect and the z feed's 2 cp); the
xellbutton site calls parseButton.  Then optional extra edits (-x NAME,..) and OPT/G site
flips (-f s1,s2).

python tools/wip/dehint/op16nat.py [-x e1,e2] [-f s1,s2] [-o out.c] [-v [fn]]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = open(optlib.SRC).read()

CHAIN = '''	else if (!strnicmp(s, "wirelessx", 9))
		b = 0x55;
	else if (!strnicmp(s, "wiredx", 6)) {
		if (!strnicmp(s, "wiredxb1", 8))
			b = 0x59;
		else if (!strnicmp(s, "wiredxb2", 8))
			b = 0x58;
		else if (!strnicmp(s, "wiredxb3", 8))
			b = 0x5a;
		else if (!strnicmp(s, "wiredxf1", 8))
			b = 0x56;
		else if (!strnicmp(s, "wiredxf2", 8))
			b = 0x57;
		else
			b = 0x5a;
	} else if (!strnicmp(s, "eject", 5))
		b = 0x12;
	else if (!strnicmp(s, "kiosk", 5))
		b = 0x41;
'''


def cut(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + text[j:]


def natural(text=SRC):
    t = text
    # the hand-written part and its comment
    t = cut(t, '/* parseButton after its first four names', 'int baseFileExists(')
    # parseButtonX and its comment
    t = cut(t, "/* applyIniOptions' copy of parseButton for xellbutton", 'int parseButton(const char *s)')
    a = '''	/* the part is cold (call predicted never taken), the original's split
	   call was likely: 36 is hoisted above the je only then */
	else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))
		b = 0x24;
	else
		b = parseButtonPart(s);
'''
    assert a in t
    t = t.replace(a, '''	else if (!strnicmp(s, "winbutton", 9))
		b = 0x24;
''' + CHAIN)
    a = 'xb.xellButton = parseButtonX(getIniValue("xellbutton"));'
    assert a in t
    t = t.replace(a, 'xb.xellButton = parseButton(getIniValue("xellbutton"));')
    return t


# extra edits on the natural base
X = {
    # drop rev feed for dz2 (rv2), dz1 (rv1)
    'rv2': [('			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n', '')],
    'rv1': [('			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }\n', '')],
    'ms': [('					__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n', '')],
    'ag1': [('					__asm__ goto ("" :::: dz1);\n', '')],
    'ag2': [('				__asm__ goto ("" :::: dz2);\n', '')],
    # parseButtonX's two hints moved into the shared parseButton (natural split kept)
    'pe': [('	if (!strnicmp(s, "power", 5))\n		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))',
            '	if (__builtin_expect(!strnicmp(s, "power", 5), 1))\n		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))')],
    'pz': [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if ('),
           ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
            '		b = 0x11;\n	else if (__builtin_constant_p(xb.xellButton + 1) && __builtin_constant_p(xb.xellButton + 2) > 0)\n		goto z;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n')],
    # z feed from the power-success arm instead (the power-fail head keeps its count)
    'pzs': [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if ('),
            ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
             '	{\n		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n		b = 0x11;\n	} else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n')],
    'pz2': [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if ('),
           ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
            '		b = 0x11;\n	else {\n		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n		if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n'),
            ('		b = 0x41;\n	return b;', '		b = 0x41;\n	}\n	return b;')],
    'pz3': [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if ('),
           ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
            '		b = 0x11;\n	else {\n		if (__builtin_constant_p(s + 1)) { if (__builtin_constant_p(s + 2) > 0) goto z; }\n		if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n'),
            ('		b = 0x41;\n	return b;', '		b = 0x41;\n	}\n	return b;')],
    'pz4': [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if ('),
           ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
            '		b = 0x11;\n	else {\n		if (__builtin_constant_p((int)s + 1)) { if (__builtin_constant_p((int)s + 2) > 0) goto z; }\n		if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n'),
            ('		b = 0x41;\n	return b;', '		b = 0x41;\n	}\n	return b;')],
}


OPT_RE = re.compile(r'OPT\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+)\);')
G_RE = re.compile(r'if \(!\(xb\.bootFlags & \(?(0x[0-9a-f]+|\d+)\)?\)\) optIniBoolG\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);')
AIO = SRC.index('void applyIniOptions(void)')
SITES = [m.group(1) for m in OPT_RE.finditer(SRC, AIO)] + [m.group(2) for m in G_RE.finditer(SRC, AIO)] + ['olddvd']


def flip(text, names):
    aio = text.index('void applyIniOptions(void)')
    head, body = text[:aio], text[aio:]
    for n in names:
        if n == 'olddvd':
            a = 'optIniBool("olddvd", 0, 4, 0);'
            assert a in body
            body = body.replace(a, 'optIniBoolG("olddvd", 0, 4, 0);')
            continue
        m = re.search(r'OPT\("%s", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+)\);' % n, body)
        if m:
            body = body[:m.start()] + 'if (!(xb.bootFlags & (%s))) optIniBoolG("%s", %s, %s, 0);' % (
                m.group(1), n, m.group(1), m.group(2)) + body[m.end():]
            continue
        m = re.search(r'if \(!\(xb\.bootFlags & \(?(0x[0-9a-f]+|\d+)\)?\)\) optIniBoolG\("%s", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);' % n, body)
        assert m, n
        body = body[:m.start()] + 'OPT("%s", %s, %s);' % (n, m.group(2), m.group(3)) + body[m.end():]
    return head + body


def feed_edit(feed, where='fail'):
    """z feed `feed` (a statement that may `goto z`) in parseButton: 'fail' at the head of
    the power-fail arm, 'succ' in the power-success arm"""
    if where == 'in':
        # z inside the feed's then-arm (its next block: no early-return prediction on the
        # feed edge); `!s` jumps there.  FEED is the condition only.
        return [('	if (!s)\n		return 0;\n	if (', '	if (!s)\n		goto z;\n	if ('),
                ('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
                 '		b = 0x11;\n	else {\n		if (%s) {\nz:\n			return 0;\n		}\n		if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n' % feed),
                ('		b = 0x41;\n	return b;', '		b = 0x41;\n	}\n	return b;')]
    e = [('	if (!s)\n		return 0;\n	if (', '	if (!s) {\nz:\n		return 0;\n	}\n	if (')]
    if where == 'fail':
        e += [('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
               '		b = 0x11;\n	else {\n		%s\n		if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n' % feed),
              ('		b = 0x41;\n	return b;', '		b = 0x41;\n	}\n	return b;')]
    else:
        e += [('		b = 0x11;\n	else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n',
               '	{\n		%s\n		b = 0x11;\n	} else if (!strnicmp(s, "remopower", 9))\n		b = 0x20;\n' % feed)]
    return e


def edits(t, names):
    for n in names:
        if n.startswith('feed'):
            X[n] = feed_edit(os.environ[n.upper()], os.environ.get(n.upper() + '_AT', 'fail'))
        for a, b in X[n]:
            assert a in t, n
            t = t.replace(a, b)
    return t


def main():
    a = sys.argv[1:]
    t = natural()
    if '-x' in a:
        t = edits(t, a[a.index('-x') + 1].split(','))
    if '-f' in a:
        t = flip(t, a[a.index('-f') + 1].split(','))
    if '-o' in a:
        open(a[a.index('-o') + 1], 'w', newline='\n').write(t)
    if '-v' in a:
        i = a.index('-v')
        optlib.vdiff(t, only=a[i + 1] if i + 1 < len(a) else None)
    else:
        print(optlib.fmt(optlib.score_text(t)))


if __name__ == '__main__':
    main()
