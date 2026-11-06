"""mode_client attempt 15: pairs (or triples with -n 3) of single trick removals
(mc12rm.PATS + mc13neg.EXTRA) with the vrp1 block count corrected (mc15k.add, k =
TARGET - c7 thread target, 0..8), scored.  BASE must be a k = 0 text (help test in one `||`).

python tools/wip/dehint/mc15pairs.py BASE_k0.c [-j 4] [-n 2] [-t 205] [-only a,b] [-o DIR]
  -only: substrings; every combination must contain at least one edit matching one of them"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12rm, mc13neg, mc14filt, mc15k


def edits(t):
    eds = []
    s0 = t.index('static void clientEraseBlockI(')
    for kind, rx, rep in mc12rm.PATS:
        for m in re.finditer(rx, t):
            if m.start() >= s0:
                eds.append(('%s@%d' % (kind, m.start()), m.start(), m.end(), re.sub(rx, rep, m.group(0))))
    for k, o, n in mc13neg.EXTRA:
        if o in t:
            i = t.index(o)
            eds.append((k, i, i + len(o), n))
    return eds


def apply(t, es):
    x = t
    for k, s, e, n in sorted(es, key=lambda z: -z[1]):
        x = x[:s] + n + x[e:]
    return x


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    n = int(a[a.index('-n') + 1]) if '-n' in a else 2
    tgt = int(a[a.index('-t') + 1]) if '-t' in a else 205
    only = a[a.index('-only') + 1].split(',') if '-only' in a else None
    odir = a[a.index('-o') + 1] if '-o' in a else None
    eds = edits(t)
    combos = []
    for c in itertools.combinations(eds, n):
        sp = sorted(c, key=lambda z: z[1])
        if any(sp[i][2] > sp[i + 1][1] for i in range(len(sp) - 1)):
            continue
        if only and not any(o in e[0] for e in c for o in only):
            continue
        combos.append(c)
    print(len(eds), 'edits', len(combos), 'combinations', flush=True)

    def one(c):
        x = apply(t, c)
        name = ' + '.join(e[0] for e in c)
        try:
            x0 = mc14filt.c7x(mc12vrp.threads(x))
        except Exception:
            return name, None, None, None
        if x0 is None or not 0 <= tgt - x0 <= 8:
            return name, x0, None, None
        y = mc15k.add(x, tgt - x0)
        if y is None:
            return name, x0, None, None
        return name, tgt - x0, mc1lib.score_text(y, []), y
    if odir:
        os.makedirs(odir, exist_ok=True)
    with ThreadPoolExecutor(jobs) as ex:
        for name, k, s, y in ex.map(one, combos):
            if s is None:
                print('skip', k, name, flush=True)
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, 'k%d' % k, name, flush=True)
            if d == 0 and odir:
                open(os.path.join(odir, 'hit_%d.c' % abs(hash(name))), 'w', newline='\n').write('/* %s */\n' % name + y)


if __name__ == '__main__':
    main()
