"""mode_client attempt 10: mc9loop with the AT-label list edits (mc10edits) as a repair.

Each removal (mc9loop.removals) alone; then, if not IDENTICAL and within -m lines:
  at:      one AT(x) label added to a list (mc10edits, 278 or so),
  default: the default case's feeds before/after its log call (mc9rep),
  perm:    fail's feeds (mc9fail), less: one cp(V + N) -> cp(V),
and within -ml lines: default x at, less x at (two steps), mc8comp's lists, less pairs.
The first IDENTICAL result is banked as OUTDIR/sNN.c and the loop starts over.

python tools/wip/dehint/mc10loop.py BASE.c OUTDIR [-m 40] [-ml 24] [-j 4] [-only RX] [-skip RX] [-la]
  -la: also less x at (6000 or so per removal, found nothing in attempt 10)"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l, mc8comp, mc9loop, mc9rep, mc10edits


def at(x):
    return [v for _, v in mc10edits.variants(x)]


def two(first):
    def gen(x):
        out = []
        for y in first(x):
            out += at(y)
        return out
    return gen


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    odir = a[1]
    os.makedirs(odir, exist_ok=True)
    mx = int(a[a.index('-m') + 1]) if '-m' in a else 40
    ml = int(a[a.index('-ml') + 1]) if '-ml' in a else 24
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    only = re.compile(a[a.index('-only') + 1]) if '-only' in a else None
    skip = re.compile(a[a.index('-skip') + 1]) if '-skip' in a else None
    while True:
        cnt = mc1.count(t)['total']
        rs = [r for r in mc9loop.removals(t) if (not only or only.search(r[0])) and not (skip and skip.search(r[0]))]
        ss = mc9loop.score([r[1] for r in rs], jobs)
        order = sorted(range(len(rs)), key=lambda i: -1 if ss[i].get('identical') else ss[i].get('total', 99999))
        print('== base', cnt, ' '.join('%s:%s' % (rs[i][0], 0 if ss[i].get('identical') else ss[i].get('total')) for i in order[:16]), flush=True)
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
            reps = [('at', at), ('default', mc9rep.default_variants), ('perm', mc9loop.perms),
                    ('less', lambda x: mc9loop.less(x, 1))]
            if s['total'] <= ml:
                reps += [('default+at', two(mc9rep.default_variants))] + ([('less+at', two(lambda x: mc9loop.less(x, 1)))] if '-la' in a else []) + [
                         ('lists', lambda x: [mc7j2l.apply(x, ed) for _, ed in mc8comp.edits(x)])]
            better = []
            for rep, gen in reps:
                cands = gen(r)
                cs = mc9loop.score(cands, jobs)
                x = mc9loop.first_hit(cands, cs)
                best = min([c.get('total', 99999) for c in cs if 'compile' not in c] or [99999])
                print('  ', name, rep, len(cands), 'HIT' if x else 'best %d' % best, flush=True)
                if x:
                    hit = (name + '+' + rep, x)
                    break
                if best < s['total'] and rep in ('perm', 'less', 'default', 'at'):
                    better.append((best, rep, cands[[c.get('total', 99999) for c in cs].index(best)]))
            # second step on the repairs that improved the removal: at, default, less on each
            for best, rep, y in sorted(better, key=lambda b: b[0])[:2] if not hit else []:
                for rep2, gen in (('at', at), ('default', mc9rep.default_variants), ('less', lambda x: mc9loop.less(x, 1)), ('perm', mc9loop.perms)):
                    if rep2 == rep:
                        continue
                    cands = gen(y)
                    cs = mc9loop.score(cands, jobs)
                    x = mc9loop.first_hit(cands, cs)
                    b2 = min([c.get('total', 99999) for c in cs if 'compile' not in c] or [99999])
                    print('  ', name, rep + '(%d)+' % best + rep2, len(cands), 'HIT' if x else 'best %d' % b2, flush=True)
                    if x:
                        hit = (name + '+' + rep + '+' + rep2, x)
                        break
                if hit:
                    break
            if hit:
                break
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
