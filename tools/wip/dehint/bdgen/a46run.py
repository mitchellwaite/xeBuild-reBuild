"""Attempt 46: score variants of attempt 45's n1 (build/bd/a46/n1.c, written by
`python tools/wip/dehint/bdgen/a45lib.py build/bd/a46/n1.c fb=con2 sz=and3 off=etype+cp+lab_t5le`
on src as of d1bcd1e6: a45lib reads src/build.c, which attempt 46 replaced, so run it from a checkout
of that commit.  src after attempt 46 is n1 re-indented, cleaned up and with the devgl hot label;
a46_m1hints.py and a46_devgl.py read src/build.c itself).

python tools/wip/dehint/bdgen/a46run.py <script.py> [-p 98,99] [-k label]
  script.py defines V = {label: [(old, new), ...]} (applied in order to n1's text; old must occur),
  or V = {label: fn(text) -> text}.  Prints loose/strict per function for each (label, p); -k writes
  that label's text to build/bd/a46/<label>.c."""
import importlib.util, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdlib, bdrun

N1 = os.path.join(bdlib.R, 'build', 'bd', 'a46', 'n1.c')


def apply(t, v):
    if callable(v):
        return v(t)
    for a, b in v:
        t = bdrun.sub(t, a, b, 1)
    return t


def main():
    a = sys.argv[1:]
    ps = [99]
    keep = None
    if '-p' in a:
        i = a.index('-p'); ps = [int(x) for x in a[i + 1].split(',')]; del a[i:i + 2]
    if '-k' in a:
        i = a.index('-k'); keep = a[i + 1]; del a[i:i + 2]
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base = open(getattr(m, 'BASE', N1), newline='').read()
    jobs = []
    for lab, v in m.V.items():
        try:
            t = apply(base, v)
        except ValueError as e:
            print(lab, 'SUBFAIL', e); continue
        if lab == keep:
            open(os.path.join(os.path.dirname(N1), lab + '.c'), 'w', newline='\n').write(t)
        for p in ps:
            jobs.append((lab, p, t))

    def one(j):
        lab, p, t = j
        fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
        return lab, p, bdrun.score(t, fl)
    with ThreadPoolExecutor(4) as ex:
        for lab, p, r in ex.map(one, jobs):
            if 'err' in r:
                print(lab, p, 'ERR', r['err'][:300]); continue
            if r['identical']:
                print('%-24s p%-3d IDENTICAL' % (lab, p), flush=True); continue
            print('%-24s p%-3d L%-4d S%-4d %s %s' % (lab, p, sum(r['L'].values()), sum(r['S'].values()),
                  ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])), flush=True)


if __name__ == '__main__':
    main()
