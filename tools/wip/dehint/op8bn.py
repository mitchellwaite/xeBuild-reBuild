"""Attempt 8: one shared reader for the button names after "power" (buttonName), called by
parseButton and parseButtonX, so gcc's own ipa-split of it replaces the hand-written
_parseButton.part.0.

python tools/wip/dehint/op8bn.py [-top N] [-show KEY]
KEY = <form>_<wexp>_<pexp>_<z>
  form: b  else-if chain setting b, `return b`      r  `if (...) return v;` chain
        bx b with the part names nested in a final else block
  wexp: E winbutton expect kept, N none
  pexp: E parseButtonX power expect kept, N none
  z:    Z z feed kept, N none"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

HEAD = [('"remopower", 9', '0x20'), ('"remox", 5', '0x22'), ('"winbutton", 9', '0x24')]
PART = '''	if (!strnicmp(s, "wirelessx", 9))
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
ZF = '\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'


def name_fn(form, wexp, guard='N'):
    t = '/* a button name other than power */\nstatic int buttonName(const char *s)\n{\n\tint b = 0;\n\n'
    if guard == 'G':
        t += '\tif (!s)\n\t\treturn 0;\n'
    for k, (n, v) in enumerate(HEAD):
        c = '!strnicmp(s, %s)' % n
        if k == 2 and wexp == 'E':
            c = '__builtin_expect(%s, 1)' % c
        if form == 'r':
            t += '\tif (%s)\n\t\treturn %s;\n' % (c, v)
        else:
            t += '\t%s (%s)\n\t\tb = %s;\n' % ('if' if k == 0 else 'else if', c, v)
    if form == 'r':
        t += PART
    elif form == 'bx':
        t += '\telse {\n' + PART.replace('\n\t', '\n\t\t').replace('\tif', '\t\tif', 1) + '\t}\n'
    else:
        t += '\telse ' + PART.lstrip('\t')
    t += '\treturn b;\n}\n'
    return t


def pbx(pexp, z):
    c = '!strnicmp(s, "power", 5)'
    if pexp == 'E':
        c = '__builtin_expect(%s, 1)' % c
    t = 'static int parseButtonX(const char *s)\n{\n\tint b = 0;\n\n'
    t += '\tif (!s) {\nz:\n\t\treturn 0;\n\t}\n' if z == 'Z' else '\tif (!s)\n\t\treturn 0;\n'
    t += '\tif (%s) {\n\t\tb = 0x11;\n\t} else {\n' % c
    if z == 'Z':
        t += ZF
    t += '\t\tb = buttonName(s);\n\t}\n\treturn b;\n}\n'
    return t


PB = '''int parseButton(const char *s)
{
	int b = 0;

	if (!s)
		return 0;
	if (!strnicmp(s, "power", 5))
		b = 0x11;
	else
		b = buttonName(s);
	return b;
}
'''


def make(base, key):
    ks = key.split('_')
    form, wexp, pexp, z = ks[:4]
    guard = ks[4] if len(ks) > 4 else 'N'
    i = base.index('/* parseButton after its first four names')
    j = base.index('int baseFileExists(')
    t = base[:i] + base[j:]
    i = t.index('/* applyIniOptions\' copy of parseButton')
    j = t.index('/* optIniInt\'s body for applyIniOptions')
    return t[:i] + name_fn(form, wexp, guard) + '\n' + pbx(pexp, z) + '\n' + PB + '\n' + t[j:]


def main():
    a = sys.argv[1:]
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = a[a.index('-show') + 1]
        out = os.path.join(optlib.BUILD, 'a8', 'op8bn_%s.c' % k)
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    ks = ['_'.join(x) for x in itertools.product(['b', 'r'], 'EN', 'EN', 'ZN', 'GN')]
    with ThreadPoolExecutor(8) as p:
        res = list(p.map(lambda k: (k, optlib.score_text(make(base, k))), ks))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9) if not x[1].get('identical') else -1)
    for f, r in res[:top]:
        print('%-10s %s' % (f, optlib.fmt(r)[:160]))


if __name__ == '__main__':
    main()
