#!/usr/bin/env python3
"""Attempt 18: parseButtonX (power expect, z feed) with a constant extra argument.

python tools/wip/dehint/op18bx.py [variant ..] [-o out.c]   (no variant: all)

Each variant replaces parseButtonX's definition and its call in applyIniOptions; scores with
optlib (reference build/op/reference.o)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = open(optlib.SRC).read()
I = SRC.index('static int parseButtonX(const char *s)')
J = SRC.index('\nint parseButton(const char *s)', I)
CALL = 'xb.xellButton = parseButtonX(getIniValue("xellbutton"));'
assert CALL in SRC

PE = '__builtin_expect(!strnicmp(s, "power", 5), 1)'
PN = '!strnicmp(s, "power", 5)'
Z = '\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'

TAIL = '''		if (!strnicmp(s, "remopower", 9))
			b = 0x20;
		else if (!strnicmp(s, "remox", 5))
			b = 0x22;
		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
		else
			b = parseButtonPart(s, %s);
'''


def cur(pe=True, z=True, sig='const char *s', ret0='0', part='0', init='0', extra_end=''):
    return ('static int parseButtonX(%s)\n{\n\tint b = %s;\n\n\tif (!s) {\nz:\n\t\treturn %s;\n\t}\n'
            '\tif (%s) {\n\t\tb = 0x11;\n\t} else {\n%s%s\t}\n%s\treturn b;\n}\n') % (
        sig, init, ret0, PE if pe else PN, Z if z else '', TAIL % part, extra_end)


V = {}
# baselines
V['cur'] = (cur(), None)
V['noz'] = (cur(z=False), None)
V['nope'] = (cur(pe=False), None)
V['none'] = (cur(pe=False, z=False), None)
# def argument (always 0)
for pe in (0, 1):
    for z in (0, 1):
        k = ('pe' if pe else '') + ('z' if z else '')
        V['d_ret_' + k] = (cur(pe, z, 'const char *s, int def', 'def', 'def'), '0')
        V['d_init_' + k] = (cur(pe, z, 'const char *s, int def', 'b', 'def', 'def'), '0')
        V['d_initp_' + k] = (cur(pe, z, 'const char *s, int def', 'b', '0', 'def'), '0')
        V['d_ifb_' + k] = (cur(pe, z, 'const char *s, int def', '0', '0', '0',
                                '\tif (!b)\n\t\tb = def;\n'), '0')
        V['d_ifbr_' + k] = (cur(pe, z, 'const char *s, int def', 'def', 'def', '0',
                                 '\tif (!b)\n\t\tb = def;\n'), '0')
        V['d_tern_' + k] = (cur(pe, z, 'const char *s, int def', '0', '0', '0').replace(
            '\treturn b;\n}', '\treturn b ? b : def;\n}'), '0')


# a test on the constant argument as the z feed (folds after the IPA inline)
for k, zt in {'zd': 'if (def) goto z;', 'zdn': 'if (!def) goto z;', 'zd1': 'if (def > 0) goto z;',
              'zdr': 'if (def) return def;', 'zdm': 'if (def < 0) goto z;', 'zdeq': 'if (def == 1) goto z;'}.items():
    for pe in (0, 1):
        for c in ('0', '1'):
            V['%s_%s%s' % (k, 'pe' if pe else 'np', '' if c == '0' else '_c1')] = (
                cur(pe, False, 'const char *s, int def').replace(
                    '\t\tif (!strnicmp(s, "remopower"', '\t\t%s\n\t\tif (!strnicmp(s, "remopower"' % zt, 1), c)


PBDEF = 'int parseButton(const char *s)\n{\n\tint b = 0;\n'
assert PBDEF in SRC
PBEND = '\t\tb = parseButtonPart(s, 0);\n\treturn b;\n}\n'


def shared(name):
    """parseButton's chain as a static buttonOf(s, def); parseButton a wrapper; the
    xellbutton site (and with S2 the other two) calls buttonOf directly"""
    t = SRC[:I] + SRC[J + 1:]
    k = t.index(PBDEF)
    e = t.index(PBEND, k) + len(PBEND)
    body = t[k:e]
    dv = name in ('S1d', 'S2d', 'S3d')
    nb = body.replace('int parseButton(const char *s)', 'static int buttonOf(const char *s, int def)')
    if dv:
        nb = nb.replace('\tint b = 0;\n', '\tint b = def;\n').replace('\t\treturn 0;\n', '\t\treturn def;\n', 1)
    wrap = '\nint parseButton(const char *s)\n{\n\treturn buttonOf(s, 0);\n}\n'
    if name.startswith('S3'):
        wrap = ''
    t = t[:k] + nb + wrap + t[e:]
    t = t.replace(CALL, 'xb.xellButton = buttonOf(getIniValue("xellbutton"), 0);')
    if name.startswith(('S2', 'S3')):
        t = t.replace('parseButton(getIniValue("xellbutton2"))', 'buttonOf(getIniValue("xellbutton2"), 0)')
        t = t.replace('parseButton(getIniValue("dualboot"))', 'buttonOf(getIniValue("dualboot"), 0)')
    if name.startswith('S3'):
        # parseButton stays global, its own copy; the ini sites use the helper
        t = t.replace('static int buttonOf(', 'int parseButton(const char *s)\n{\n\treturn buttonOf(s, 0);\n}\n\nstatic int buttonOf(', 0)
    return t


for n in ('S1', 'S1d', 'S2', 'S2d'):
    V[n] = (None, None)


def make(name):
    if name.startswith('S'):
        return shared(name)
    body, arg = V[name]
    t = SRC[:I] + body + SRC[J:]
    if arg is not None:
        t = t.replace(CALL, 'xb.xellButton = parseButtonX(getIniValue("xellbutton"), %s);' % arg)
    return t


def main():
    a = sys.argv[1:]
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    names = a or list(V)
    for n in names:
        t = make(n)
        if out:
            open(out, 'w', newline='\n').write(t)
        r = optlib.score_text(t)
        print('%-16s %s' % (n, optlib.fmt(r)), flush=True)


main()
