"""Attempt 15: which optIniBool sites use optIniBool (OPT) and which optIniBoolG.  Both give
the same code after inlining but different cold profiles (G's warning arm joins, ib's
returns), so the choice per site moves cold keys without changing code.  Swept on top of a
removal (rv2, bxz, ...) to see whether some assignment does the removed trick's job.

python tools/wip/dehint/op15site.py [-rm rv2[,bxz]] [-k K] [-all] [-only s1,s2] [-show s1,s2]
  -k K: flip up to K sites from the current assignment (default 2); -all: every subset
  -show: print the source with these sites flipped (OUT=file writes it)"""
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
OPT_RE = re.compile(r'OPT\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+)\);')
G_RE = re.compile(r'if \(!\(xb\.bootFlags & \(?(0x[0-9a-f]+|\d+)\)?\)\) optIniBoolG\("(\w+)", (0x[0-9a-f]+|\d+), (0x[0-9a-f]+|\d+), 0\);')
AIO = SRC.index('void applyIniOptions(void)')
sites = [m.group(1) for m in OPT_RE.finditer(SRC, AIO)] + [m.group(2) for m in G_RE.finditer(SRC, AIO)]
sites.append('olddvd')


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


def apply_rm(text, rms):
    for r in rms:
        for a, b in RM[r]:
            assert a in text, r
            text = text.replace(a, b)
    return text


def main():
    a = sys.argv[1:]
    rms = a[a.index('-rm') + 1].split(',') if '-rm' in a else []
    base = apply_rm(SRC, rms)
    if '-show' in a:
        t = flip(base, a[a.index('-show') + 1].split(','))
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(t)
        print(optlib.fmt(optlib.score_text(t)))
        return
    pool = sites
    if '-only' in a:
        pool = a[a.index('-only') + 1].split(',')
    K = int(a[a.index('-k') + 1]) if '-k' in a else 2
    if '-all' in a:
        K = len(pool)
    combos = [c for k in range(0, K + 1) for c in itertools.combinations(pool, k)]
    print('sites', pool, len(combos), 'combinations', 'removals', rms, flush=True)

    def run(c):
        r = optlib.score_text(flip(base, c))
        return c, r
    res = []
    with ThreadPoolExecutor(4) as ex:
        for c, r in ex.map(run, combos):
            res.append((r.get('total', 99999) if not r.get('identical') else 0, c, r))
            if r.get('identical'):
                print('IDENTICAL', c, flush=True)
    res.sort(key=lambda x: x[0])
    for s, c, r in res[:25]:
        print(s, ','.join(c) or '-', r.get('per'), ' '.join(r.get('notes', [])))


main()
