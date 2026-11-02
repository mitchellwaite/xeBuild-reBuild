"""ext.py: extends s19 search targets with non-call statements (labels before the case 4/5
hwFlags tests = blocks 110/113, the preds of 112/115) and measures singles on a base.
python ext.py BASE.json [WSET]  -> prints inj, inv, fq deltas, missing."""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc', 's19')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc', 's21'))
import search, table
table.D = os.path.join(ROOT, 'build', 'v', 'mc23')
S = search.SRC
EXTRA = {}
for nm, pat in [('h4', '\t\t\tcase 4:\n\t\t\t\tif (cinfo->hwFlags'), ('h5', '\t\t\tcase 5:\n\t\t\t\tif (cinfo->hwFlags')]:
    off = S.index(pat, search.LOOP1) + len('\t\t\tcase 4:\n\t\t\t\t')
    EXTRA[nm] = len(search.TGT); search.TGT.append(('mc', off))
for nm, pat in [('t7', 'AT(c7) if (arg == dummy)'), ('t12', 'AT(c12) if (arg == dummy)')]:
    off = S.index(pat, search.LOOP1) + len('AT(c7) ')
    EXTRA[nm] = len(search.TGT); search.TGT.append(('mc', off))
if __name__ == '__main__':
    base = [tuple(x) for x in json.load(open(sys.argv[1]))] if len(sys.argv) > 1 else []
    ws = (sys.argv[2] if len(sys.argv) > 2 else 'b,p,pp,ppp,q').split(',')
    b = table.meas(base, 'base'); print('base inv', b['inv'], b['order'])
    jobs = [base + [(t, s, w)] for t in EXTRA.values() for s in ('rok', 'fail', 'after') for w in ws]
    def one(j): return j, table.meas(j, '_'.join(map(str, j[-1])))
    with ThreadPoolExecutor(8) as ex:
        for j, r in ex.map(one, jobs):
            if r is None: print(j[-1], 'fail'); continue
            d = {k: r['fq'].get(k, 0) - b['fq'].get(k, 0) for k in set(r['fq']) | set(b['fq'])}
            print(j[-1], r['inv'], {k: v for k, v in d.items() if v}, r['needmiss'])
            print('   ', r['order'])
