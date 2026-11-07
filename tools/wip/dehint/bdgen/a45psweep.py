"""Attempt 45: the param swept on loop-form variants (a45lib.loop).  python tools/wip/dehint/bdgen/a45psweep.py
'<label>:k=v,k=v,off=a+b' ... [-p 60,70,80] ; prints loose/strict per function for each (variant, p)."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun, a45lib


def parse(spec):
    lab, _, kv = spec.partition(':')
    kw = {}
    for a in filter(None, kv.split(',')):
        k, v = a.split('=')
        if k == 'off':
            kw[k] = tuple(filter(None, v.split('+')))
        elif v in ('True', 'False'):
            kw[k] = v == 'True'
        else:
            kw[k] = v
    return lab, kw


def main():
    a = sys.argv[1:]
    ps = list(range(50, 100, 2)) + [99]
    if '-p' in a:
        i = a.index('-p'); ps = [int(x) for x in a[i + 1].split(',')]; del a[i:i + 2]
    base = bdlib.read_src()
    jobs = []
    for spec in a:
        lab, kw = parse(spec)
        t = a45lib.loop(base, **kw)
        for p in ps:
            jobs.append((lab, p, t))

    def one(j):
        lab, p, t = j
        return lab, p, bdrun.score(t, ['--param', 'builtin-expect-probability=%d' % p])
    with ThreadPoolExecutor(4) as ex:
        for lab, p, r in ex.map(one, jobs):
            if 'err' in r:
                print(lab, p, 'ERR', r['err'][:200]); continue
            if r['identical']:
                print('%-20s p%-3d IDENTICAL' % (lab, p)); continue
            print('%-20s p%-3d L%-4d S%-4d %s %s' % (lab, p, sum(r['L'].values()), sum(r['S'].values()),
                  ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])), flush=True)


if __name__ == '__main__':
    main()
