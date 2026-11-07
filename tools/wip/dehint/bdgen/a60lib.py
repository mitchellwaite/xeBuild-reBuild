"""Attempt 60: score build.o variants of src/build.c (edits as (old, new[, count]) lists or callables),
each crossed with hint sets off (bdhints names).

python tools/wip/dehint/bdgen/a60lib.py <script.py> [-p 99] [-o "set;set"] [-k label] [-f substr]
  script.py defines V = {label: [(old, new[, count]), ..] or fn(text) -> text}; -o as a58lib
  ('-' = all hints kept; default '-' and each hint alone); -f keeps only labels containing substr;
  -k writes that label's text to build/bd/a60/<label>.c.  Prints loose/strict per function."""
import importlib.util, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun, bdhints
from a58lib import score

OUT = os.path.join(bdlib.R, 'build', 'bd', 'a60')
SRCD = os.path.join(bdlib.R, 'src')


def apply(t, v):
    if callable(v):
        return v(t)
    for e in v:
        a, b = e[0], e[1]
        n = e[2] if len(e) > 2 else 1
        if t.count(a) < (n if n > 0 else 1):
            raise ValueError('not found x%d: %r' % (n, a[:70]))
        t = t.replace(a, b, n)
    return t


def main():
    a = sys.argv[1:]
    p, keep, sets, filt = 99, None, None, None
    for opt in ('-p', '-k', '-o', '-f'):
        if opt in a:
            i = a.index(opt); val = a[i + 1]; del a[i:i + 2]
            if opt == '-p': p = int(val)
            if opt == '-k': keep = val
            if opt == '-o': sets = val.split(';')
            if opt == '-f': filt = val
    sets = sets or ['-'] + list(bdhints.H)
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base = bdlib.read_src()
    fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for lab, v in m.V.items():
        if filt and filt not in lab:
            continue
        try:
            t = apply(base, v)
        except ValueError as e:
            print(lab, 'SUBFAIL', e); continue
        if lab == keep:
            open(os.path.join(OUT, lab + '.c'), 'w', newline='\n').write(t)
        for s in getattr(m, 'SETS', {}).get(lab, sets):
            try:
                tt = t if s == '-' else bdhints.off(t, *s.split(','))
            except ValueError as e:
                print('%-22s %-12s SUBFAIL %s' % (lab, s, e)); continue
            jobs.append((lab, s, tt))

    def one(j):
        lab, s, t = j
        return lab, s, score(t, fl, SRCD)
    with ThreadPoolExecutor(4) as ex:
        for lab, s, r in ex.map(one, jobs):
            if 'err' in r:
                print('%-22s %-12s ERR %s' % (lab, s, r['err'][:300].replace('\n', ' | '))); continue
            if r['identical']:
                print('%-22s %-12s IDENTICAL' % (lab, s), flush=True); continue
            print('%-22s %-12s L%-4d S%-4d %s %s' % (lab, s, sum(r['L'].values()), sum(r['S'].values()),
                  ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])), flush=True)


if __name__ == '__main__':
    main()
