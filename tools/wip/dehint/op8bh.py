"""Attempt 8: buttonName with power inside (the whole name chain), parseButton a null-check
wrapper, so gcc's ipa-split of buttonName replaces the hand-written part; parseButtonX
variants on top.

python tools/wip/dehint/op8bh.py [-show KEY]   (prints split point and .rdata head too)
KEY = <x>_<wexp>
  x: W  parseButtonX = parseButton's wrapper with the z feed before the call
     P  parseButtonX deleted, xellbutton reads through parseButton
     X  parseButtonX kept as now (own chain), calls buttonName for the rest after power
  wexp: E winbutton expect, N none"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op8bn

CH = [('"power", 5', '0x11')] + op8bn.HEAD


def bname(wexp):
    t = '/* a button name */\nstatic int buttonName(const char *s)\n{\n\tint b = 0;\n\n'
    for k, (n, v) in enumerate(CH):
        c = '!strnicmp(s, %s)' % n
        if k == 3 and wexp == 'E':
            c = '__builtin_expect(%s, 1)' % c
        t += '\t%s (%s)\n\t\tb = %s;\n' % ('if' if k == 0 else 'else if', c, v)
    t += '\telse ' + op8bn.PART.lstrip('\t')
    t += '\treturn b;\n}\n'
    return t


PB = '''int parseButton(const char *s)
{
	if (!s)
		return 0;
	return buttonName(s);
}
'''
PBX_W = '''static int parseButtonX(const char *s)
{
	if (!s) {
z:
		return 0;
	}
	if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }
	return buttonName(s);
}
'''


def make(base, key):
    x, wexp = key.split('_')
    i = base.index('/* parseButton after its first four names')
    j = base.index('int baseFileExists(')
    t = base[:i] + base[j:]
    i = t.index('/* applyIniOptions\' copy of parseButton')
    j = t.index('/* optIniInt\'s body for applyIniOptions')
    if x == 'X':
        px = op8bn.pbx('E', 'Z')
    elif x == 'W':
        px = PBX_W
    else:
        px = ''
        t = t.replace('parseButtonX(getIniValue("xellbutton"))', 'parseButton(getIniValue("xellbutton"))')
    return t[:i] + bname(wexp) + '\n' + px + '\n' + PB + '\n' + t[j:]


def diag(text):
    ok, o, d = optlib.compile_src(text, extra=['-fdump-tree-fnsplit-details'])
    out = []
    try:
        dumps = [f for f in os.listdir(d) if 'fnsplit' in f]
        if dumps:
            dt = open(os.path.join(d, dumps[0])).read()
            i = dt.find(';; Function buttonName')
            k = dt.find('Splitting function at:', i)
            if i >= 0 and k > 0:
                out.append(dt[k:k + 80].split('\n')[1])
        r = subprocess.run([optlib.bdlib.OBJDUMP, '-s', '-j', '.rdata', o], capture_output=True, text=True).stdout
        out.append(r.split('\n')[4][43:] if len(r.split('\n')) > 4 else '?')
    finally:
        optlib.cleanup(d)
    return ' | '.join(out)


def main():
    a = sys.argv[1:]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = a[a.index('-show') + 1]
        out = os.path.join(optlib.BUILD, 'a8', 'op8bh_%s.c' % k)
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    ks = [x + '_' + w for x in 'WPX' for w in 'EN']
    with ThreadPoolExecutor(6) as p:
        res = list(p.map(lambda k: (k, optlib.score_text(make(base, k)), diag(make(base, k))), ks))
    for f, r, dg in res:
        print('%-5s %-40s %s' % (f, dg, optlib.fmt(r)[:200]))


if __name__ == '__main__':
    main()
