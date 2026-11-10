#!/usr/bin/env python3
"""mode_client attempt 17: sweep a product of mc17.py's axes, scoring whole objects.

python tools/wip/dehint/mc17sw.py [-n TOP] [-log FILE] axis=v1,v2 axis=v ..
  every combination of the listed values (other axes at their first value).

Per variant: differing lines, `moved` (layout blocks out of place against the reference),
`pre` (blocks equal from the start of mode_client: the hot part comes first), `cas`
(the eleven switch cases in the reference's order: C or -), `nc` (netConnect calls: 2 in
the reference).  Sorted by lines; results are cached in build/mc/w17/cache.json by
source text."""
import hashlib, itertools, json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc17
import mc17lib as L

CACHE = os.path.join(L.BUILD, 'cache.json')
CASE = ('clientInfo()', 'netDumpNand()', 'clientKeys()', 'sendAvatarData()', 'sendCompatData()', 'clientWrite()',
        'clientReadBlocks()', 'clientWriteBlocks()', 'clientBinPatch()', 'clientPatches()', 'invalid mode')
REFC = [x[0] for x in L.chunks(L.REF)]


def caseorder(names):
    out = []
    for n in names:
        for c in CASE:
            if c in n and c not in out and 'usage' not in n:
                out.append(c)
    return out


REFCASE = caseorder(REFC)


def measure(text):
    ok, o, d = L.compile_src(text)
    try:
        if not ok:
            return {'err': o.strip().split('\n')[-1][:120]}
        idn, tot, per, notes = L.report(o)
        names = [x[0] for x in L.chunks(o)]
        pre = 0
        for a, b in zip(REFC, names):
            if a != b:
                break
            pre += 1
        return {'idn': idn, 'lines': tot, 'moved': L.laydiff(o, show=False), 'pre': pre,
                'cas': caseorder(names) == REFCASE, 'nc': ' '.join(names).count('netConnect()'),
                'fns': sorted(k for k in per if k != '_mode_client'), 'notes': notes}
    finally:
        L.cleanup(d)


def fmt(r):
    if r is None:
        return 'n/a'
    if 'err' in r:
        return 'ERR ' + r['err']
    if r['idn']:
        return 'IDENTICAL ' + ' '.join(r['notes'])
    return '%5d moved=%2d pre=%2d cas=%s nc=%d %s' % (r['lines'], r['moved'], r['pre'], 'C' if r['cas'] else '-',
                                                    r['nc'], ' '.join(r['fns']))


def run(variants, top=None, log=None, jobs=6):
    try:
        cache = json.load(open(CACHE))
    except (OSError, ValueError):
        cache = {}
    texts = {}
    for v in variants:
        t = mc17.text_of(v)
        if t is not None:
            texts[v] = t
    todo = {}
    for v, t in texts.items():
        h = hashlib.sha1(t.encode()).hexdigest()
        if h not in cache:
            todo.setdefault(h, t)
    if todo:
        with ThreadPoolExecutor(jobs) as ex:
            for h, r in zip(todo, ex.map(measure, todo.values())):
                cache[h] = r
        json.dump(cache, open(CACHE, 'w'))
    rows = [(v, cache[hashlib.sha1(t.encode()).hexdigest()]) for v, t in texts.items()]
    rows.sort(key=lambda x: (not x[1].get('idn', False), x[1].get('lines', 99999), x[1].get('moved', 99)))
    out = ['%-70s %s' % (v, fmt(r)) for v, r in rows]
    if log:
        open(log, 'w', newline='\n').write('\n'.join(out) + '\n')
    for l in out[:top]:
        print(l)
    return rows


def product(specs):
    keys, vals = [], []
    for s in specs:
        k, v = s.split('=')
        assert k in mc17.AXES, k
        for x in v.split(','):
            assert x in mc17.AXES[k], (k, x)
        keys.append(k)
        vals.append(v.split(','))
    return [','.join('%s=%s' % kv for kv in zip(keys, c)) for c in itertools.product(*vals)]


if __name__ == '__main__':
    a = sys.argv[1:]
    top = None
    if '-n' in a:
        k = a.index('-n'); top = int(a[k + 1]); del a[k:k + 2]
    log = None
    if '-log' in a:
        k = a.index('-log'); log = a[k + 1]; del a[k:k + 2]
    vs = product(a)
    print(len(vs), 'variants', flush=True)
    run(vs, top, log)
