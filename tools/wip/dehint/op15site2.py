"""Attempt 15: op15site.py with more forms per optIniBool site:
  o  OPT(name, set, clear)                         (guarded optIniBool)
  g  if (!(xb.bootFlags & set)) optIniBoolG(...)   (guarded optIniBoolG)
  uo optIniBool(name, set, clear, 0)               (no guard: the helper's own test does it)
  ug optIniBoolG(name, set, clear, 0)
  o2/g2 if (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) optIniBool[G](...)  (both
     flags tested at the site too; the helper's own tests fold)
python tools/wip/dehint/op15site2.py [-rm rv2,..] [-k K] [-forms o,g,uo,ug] [-base s=f,..]
       [-only s1,..] [-show s=f,..]
  sweeps every assignment that changes up to K sites (default 1) from the base"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = open(optlib.SRC).read()
RM = {
    'rv2': [('			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n', '')],
    'bxz': [('		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n', '')],
    'pbe': [('else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))', 'else if (!strnicmp(s, "winbutton", 9))')],
    'bxe': [('if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {', 'if (!strnicmp(s, "power", 5)) {')],
    'ms': [('					__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n', '')],
}
LINE = re.compile(r'(?:if \(!\(xb\.bootFlags & \((?:0x[0-9a-f]+|\d+)\)\) && !\(xb\.bootFlagsOff & \((?:0x[0-9a-f]+|\d+)\)\)\) optIniBool(G?)\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);'
                  r'|OPT\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+)\);'
                  r'|if \(!\(xb\.bootFlags & \(?(?:0x[0-9a-f]+|\d+)\)?\)\) optIniBoolG\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);'
                  r'|optIniBool(G?)\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);)')


def parse(text):
    """sites in applyIniOptions: name -> (form, set, clear, span)"""
    aio = text.index('void applyIniOptions(void)')
    out = {}
    for m in LINE.finditer(text, aio):
        g = (None,) + m.groups()[4:]
        if m.group(2):
            out[m.group(2)] = ('g2' if m.group(1) else 'o2', m.group(3), m.group(4), m.span())
            continue
        m2 = m
        class M:
            def group(self, i):
                return g[i]
            def span(self):
                return m2.span()
        m = M()
        if m.group(1):
            out[m.group(1)] = ('o', m.group(2), m.group(3), m.span())
        elif m.group(4):
            out[m.group(4)] = ('g', m.group(5), m.group(6), m.span())
        else:
            out[m.group(8)] = ('ug' if m.group(7) else 'uo', m.group(9), m.group(10), m.span())
    return out


def spell(n, f, st, cl):
    if f == 'o':
        return 'OPT("%s", %s, %s);' % (n, st, cl)
    if f == 'g':
        return 'if (!(xb.bootFlags & (%s))) optIniBoolG("%s", %s, %s, 0);' % (st, n, st, cl)
    if f in ('o2', 'g2'):
        return 'if (!(xb.bootFlags & (%s)) && !(xb.bootFlagsOff & (%s))) optIniBool%s("%s", %s, %s, 0);' % (st, st, 'G' if f == 'g2' else '', n, st, cl)
    if f == 'uo':
        return 'optIniBool("%s", %s, %s, 0);' % (n, st, cl)
    return 'optIniBoolG("%s", %s, %s, 0);' % (n, st, cl)


def assign(text, ch):
    ss = parse(text)
    for n, f in sorted(ch.items(), key=lambda x: -ss[x[0]][3][0]):
        _, st, cl, (a, b) = ss[n]
        text = text[:a] + spell(n, f, st, cl) + text[b:]
    return text


def apply_rm(text, rms):
    for r in rms:
        for a, b in RM[r]:
            assert a in text, r
            text = text.replace(a, b)
    return text


def kv(s):
    return dict(x.split('=') for x in s.split(',') if x)


def main():
    a = sys.argv[1:]
    rms = a[a.index('-rm') + 1].split(',') if '-rm' in a else []
    base = apply_rm(SRC, rms)
    if '-base' in a:
        base = assign(base, kv(a[a.index('-base') + 1]))
    if '-show' in a:
        t = assign(base, kv(a[a.index('-show') + 1]))
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(t)
        print(optlib.fmt(optlib.score_text(t)))
        return
    ss = parse(base)
    pool = a[a.index('-only') + 1].split(',') if '-only' in a else sorted(ss)
    forms = a[a.index('-forms') + 1].split(',') if '-forms' in a else ['o', 'g', 'uo', 'ug']
    K = int(a[a.index('-k') + 1]) if '-k' in a else 1
    combos = [{}]
    for k in range(1, K + 1):
        for names in itertools.combinations(pool, k):
            alts = [[f for f in forms if f != ss[n][0]] for n in names]
            for fs in itertools.product(*alts):
                combos.append(dict(zip(names, fs)))
    print('base', {n: ss[n][0] for n in sorted(ss)}, 'removals', rms, len(combos), 'combinations', flush=True)

    def run(c):
        return c, optlib.score_text(assign(base, c))
    res = []
    with ThreadPoolExecutor(4) as ex:
        for c, r in ex.map(run, combos):
            sc = 0 if r.get('identical') else r.get('total', 99999)
            res.append((sc, c, r))
            if r.get('identical') and c:
                print('IDENTICAL', c, flush=True)
    res.sort(key=lambda x: x[0])
    for s, c, r in res[:int(os.environ.get('TOP', 30))]:
        print(s, ','.join('%s=%s' % x for x in sorted(c.items())) or '-', r.get('per'), ' '.join(r.get('notes', [])))


main()
