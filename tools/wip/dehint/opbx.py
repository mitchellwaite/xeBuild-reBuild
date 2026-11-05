"""opbx.py [-o DIR] [names..]: reduced parseButtonX bodies on top of src/options.c, scored with
optlib.  Each variant replaces the whole parseButtonX definition."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

HDR = 'static int parseButtonX(const char *s)\n{'
TAIL = '''		else
			b = parseButtonPart(s);
'''
CHAIN = '''		if (!strnicmp(s, "remopower", 9))
			b = 0x20;
		else if (!strnicmp(s, "remox", 5))
			b = 0x22;
		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
''' + TAIL
Z = '''		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2)) goto z; if (__builtin_constant_p(xb.xellButton + 3)) goto z; }
'''
Z1 = '''		if (__builtin_constant_p(xb.xellButton + 1)) goto z;
'''
Z2 = '''		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2)) goto z; }
'''


def body(pexp=True, z=Z, dx=True):
    p = '__builtin_expect(!strnicmp(s, "power", 5), 1)' if pexp else '!strnicmp(s, "power", 5)'
    s = HDR + '''
	int b = 0;

	if (!s) {
z:
		return 0;
	}
	if (%s) {
		b = 0x11;
''' % p
    if dx is True:
        s += '''		if (__builtin_expect(__builtin_constant_p(xb.xellButton + 5), 1)) goto dx;
bx: ;
	} else {
		__asm__ goto ("" :::: dxc);
'''
    elif dx:
        # cheaper dummies: an asm goto out of the power arm, flow returned by a dead test
        s += '\t\t__asm__ goto ("" :::: dx);\nbx: ;\n\t} else {\n'
    else:
        s += '	} else {\n'
    s += z + CHAIN + '\t}\n\treturn b;\n'
    if dx == 'ag':
        s += '''dx:
	__asm__ volatile ("" :: "i"(3));
	b = 0x11;
	if (__builtin_constant_p(xb.xellButton + 6))
		goto bx;
	__builtin_unreachable();
'''
    elif dx == 'ag_nopin':
        s += '''dx:
	b = 0x11;
	if (__builtin_constant_p(xb.xellButton + 6))
		goto bx;
	__builtin_unreachable();
'''
    elif dx == 'ag_back':
        s += '''dx:
	__asm__ volatile ("" :: "i"(3));
	goto bx;
'''
    elif dx == 'ag_back2':
        s += '''dx:
	goto bx;
'''
    if dx is True:
        s += '''dxc: __attribute__((cold));
	goto dx;
dx:
	__asm__ volatile ("" :: "i"(3));
	b = 0x11;
	if (__builtin_constant_p(xb.xellButton + 6))
		goto bx;
	__builtin_unreachable();
'''
    return s + '}\n'


V = {
    'cur': body(),
    'nodx': body(dx=False),
    'nodx_z1': body(dx=False, z=Z1),
    'nodx_z2': body(dx=False, z=Z2),
    'nodx_noz': body(dx=False, z=''),
    'z1': body(z=Z1),
    'z2': body(z=Z2),
    'noz': body(z=''),
    'nopexp': body(pexp=False),
}
FEED = 'if (__builtin_expect(__builtin_constant_p(xb.xellButton + 5), 1)) goto dx;'
PIN = '	__asm__ volatile ("" :: "i"(3));\n	b = 0x11;'
V['d_noexp'] = V['cur'].replace(FEED, 'if (__builtin_constant_p(xb.xellButton + 5)) goto dx;')
V['d_nopin'] = V['cur'].replace(PIN, '	b = 0x11;')
V['d_both'] = V['d_noexp'].replace(PIN, '	b = 0x11;')
V['d_nob'] = V['cur'].replace(PIN, '	__asm__ volatile ("" :: "i"(3));')
V['d_nob_nopin'] = V['cur'].replace(PIN, '')
V['d_noexp_nob'] = V['d_noexp'].replace(PIN, '	__asm__ volatile ("" :: "i"(3));')
V['d_all'] = V['d_noexp'].replace(PIN, '')
B = V['d_nopin']
V['e_nocold'] = B.replace('__asm__ goto ("" :::: dxc);', '__asm__ goto ("" :::: dx);').replace('dxc: __attribute__((cold));\n\tgoto dx;\n', '')
V['e_cold_dx'] = B.replace('__asm__ goto ("" :::: dxc);', '__asm__ goto ("" :::: dx);').replace('dxc: __attribute__((cold));\n\tgoto dx;\ndx:\n', 'dx: __attribute__((cold));\n')
V['e_z2'] = B.replace(Z, Z2)
V['e_z1'] = B.replace(Z, Z1)
V['e_noz'] = B.replace(Z, '')
V['e_unr'] = B.replace('	if (__builtin_constant_p(xb.xellButton + 6))\n		goto bx;\n	__builtin_unreachable();\n', '	goto bx;\n')
for m in ('ag', 'ag_nopin', 'ag_back', 'ag_back2'):
    V[m] = body(dx=m)
    V[m + '_z2'] = body(dx=m, z=Z2)
    V[m + '_noz'] = body(dx=m, z='')
    V[m + '_nopexp'] = body(dx=m, pexp=False)


def make(name):
    t = optlib.read_src(optlib.SRC)
    i = t.index(HDR)
    j = t.index('\n}\n', i) + 3
    return t[:i] + V[name] + t[j:]


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
        os.makedirs(out, exist_ok=True)
    names = a or list(V)

    def one(n):
        t = make(n)
        if out:
            open(os.path.join(out, n + '.c'), 'w', newline='\n').write(t)
        return n, optlib.score_text(t)
    with ThreadPoolExecutor(6) as p:
        for n, r in p.map(one, names):
            print('%-10s %s' % (n, optlib.fmt(r)), flush=True)
