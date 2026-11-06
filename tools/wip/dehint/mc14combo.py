"""mode_client attempt 14: cross product of edit groups (one edit from each group, an empty
name '-' means none), with the vrp1 block-count shift, thread order and score of each.

python tools/wip/dehint/mc14combo.py BASE.c GROUPS.py [-j 4] [-noscore] [-o OUTDIR]
GROUPS.py defines GROUPS = [[(name, old, new), ...], ...]; edits apply in group order, each
old must occur in the text as edited so far (first occurrence replaced).  IDENTICAL texts
are written to OUTDIR/<names>.c."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt


def xs(th):
    return sorted(int(x) for _, _, x in th[:3] if x != '?')


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    g = {}
    exec(open(a[1]).read(), g)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    out = a[a.index('-o') + 1] if '-o' in a else None
    if out:
        os.makedirs(out, exist_ok=True)
    base = xs(mc12vrp.threads(t))
    print('base', base, flush=True)
    combos = list(itertools.product(*g['GROUPS']))

    def one(c):
        x = t
        names = []
        for name, old, new in c:
            if name == '-':
                continue
            if old not in x:
                return '+'.join(n for n, _, _ in c), None, 'missing ' + name, None
            x = x.replace(old, new, 1)
            names.append(name)
        nm = '+'.join(names) or 'base'
        try:
            th = mc12vrp.threads(x)
        except Exception:
            return nm, None, 'err', None
        s = None
        if '-noscore' not in a:
            s = mc1lib.score_text(x, [])
            if s.get('identical') and out:
                open(os.path.join(out, nm + '.c'), 'w', newline='\n').write(x)
        return nm, th, xs(th), s
    with ThreadPoolExecutor(jobs) as ex:
        for nm, th, v, s in ex.map(one, combos):
            if th is None:
                print(nm, v, flush=True)
                continue
            sh = v[0] - base[0] if v and base else '?'
            sc = '' if s is None else ('IDENTICAL' if s.get('identical') else s.get('total', s))
            print('%+d' % sh if sh != '?' else sh, 'GOOD' if mc12filt.good(th) else 'bad ', v, sc, nm, flush=True)


if __name__ == '__main__':
    main()
