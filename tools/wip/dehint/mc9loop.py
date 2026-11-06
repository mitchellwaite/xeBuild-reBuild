"""mode_client attempt 9: greedy removal loop with count-neutral repairs.

Removals are generated from the text (every 1-term cp feed, every `&& cp(...)` term, a
1-term mode-chain arm, plus mc8comp's named non-cp removals).  Each removal is scored
alone, then (if not IDENTICAL and within -m lines) repaired with:
  perm: fail's feeds reordered / moved after the log call (mc9fail),
  less: one `cp(V + N)` -> `cp(V)` toggle (mc8tmp), then pairs if -k 2.
The first IDENTICAL result is banked as OUTDIR/sNN.c and the loop starts over.

python tools/wip/dehint/mc9loop.py BASE.c OUTDIR [-m 40] [-k 1] [-ml 14] [-j 8] [-only RX]
  -ml: removals within this many lines also get every single list edit and less pairs"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l, mc8comp, mc8tmp, mc9fail

CP = r'__builtin_constant_p\([^()]*(?:\([^()]*\))?[^()]*\)'


def removals(t):
    out = []
    s = t.index('static void clientEraseBlockI(')
    for m in re.finditer(r' ?if \(' + CP + r'\) goto (\w+);', t[s:]):
        out.append(('feed:%s@%d' % (m.group(1), s + m.start()), t[:s + m.start()] + t[s + m.end():]))
    for m in re.finditer(r' && (?:\(char \*\))?' + CP + r'(?: == \(char \*\)1)?', t[s:]):
        out.append(('term@%d' % (s + m.start()), t[:s + m.start()] + t[s + m.end():]))
    for m in re.finditer(r'if \(' + CP + r'\) mode = (\d+); else ', t[s:]):
        out.append(('arm%s' % m.group(1), t[:s + m.start()] + t[s + m.end():]))
    for n in mc8comp.REMOVALS:
        if n == 'none' or n.startswith(('arm', 'c9', 't5', 'c11', 'c3', 's5', 'dtg', 't4', 'u2', 'ndl', 'k61l', 'dyfeed', 'ybkfeed')):
            continue
        r = mc8comp.remove(t, n)
        if r:
            out.append((n, r))
    return out


def perms(t):
    try:
        pre, feeds, log, post = mc9fail.split(t)
    except (ValueError, AssertionError):
        return []
    res = set()
    for perm in itertools.permutations(feeds):
        for cut in range(len(feeds) + 1):
            res.add(mc9fail.render(pre, list(perm[:cut]), log, list(perm[cut:]), post))
    res.discard(t)
    return sorted(res)


def less(t, k):
    ss = [x for x in mc8tmp.sites(t) if x[0].startswith('less')]
    out = []
    for kk in range(1, k + 1):
        for comb in itertools.combinations(ss, kk):
            out.append(mc8tmp.apply(t, [c[1] for c in comb]))
    return out


def score(ts, jobs):
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(lambda x: mc1lib.score_text(x, []), ts))


def first_hit(ts, ss):
    for x, s in zip(ts, ss):
        if s.get('identical'):
            return x
    return None


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    odir = a[1]
    os.makedirs(odir, exist_ok=True)
    mx = int(a[a.index('-m') + 1]) if '-m' in a else 40
    k = int(a[a.index('-k') + 1]) if '-k' in a else 1
    ml = int(a[a.index('-ml') + 1]) if '-ml' in a else 14
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 8
    only = re.compile(a[a.index('-only') + 1]) if '-only' in a else None
    while True:
        cnt = mc1.count(t)['total']
        rs = [r for r in removals(t) if not only or only.search(r[0])]
        ss = score([r[1] for r in rs], jobs)
        order = sorted(range(len(rs)), key=lambda i: -1 if ss[i].get('identical') else ss[i].get('total', 99999))
        print('== base', cnt, ' '.join('%s:%s' % (rs[i][0], 0 if ss[i].get('identical') else ss[i].get('total')) for i in order[:14]), flush=True)
        hit = None
        for i in order:
            name, r = rs[i]
            s = ss[i]
            if 'compile' in s:
                continue
            if s.get('identical'):
                hit = (name, r)
                break
            if s['total'] > mx:
                break
            reps = [('perm', perms), ('less', lambda x: less(x, k))]
            if s['total'] <= ml:
                reps += [('lists', lambda x: [mc7j2l.apply(x, ed) for _, ed in mc8comp.edits(x)]),
                         ('less2', lambda x: less(x, 2)[len(less(x, 1)):])]
            for rep, gen in reps:
                cands = gen(r)
                cs = score(cands, jobs)
                x = first_hit(cands, cs)
                best = min([c.get('total', 99999) for c in cs if 'compile' not in c] or [99999])
                print('  ', name, rep, len(cands), 'HIT' if x else 'best %d' % best, flush=True)
                if x:
                    hit = (name + '+' + rep, x)
                    break
            if hit:
                break
            # perm then less on the best perms
        if not hit:
            print('stuck at', cnt, flush=True)
            break
        t = hit[1]
        n2 = mc1.count(t)['total']
        p = os.path.join(odir, 's%d.c' % n2)
        open(p, 'w', newline='\n').write(t)
        print('BANK', hit[0], cnt, '->', n2, p, flush=True)
        if n2 >= cnt:
            print('count did not drop, stop', flush=True)
            break


if __name__ == '__main__':
    main()
