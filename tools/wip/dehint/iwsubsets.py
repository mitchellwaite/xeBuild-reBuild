"""python tools/wip/dehint/iwsubsets.py name1 name2 ...: score every subset of these iwtricks removals
(base IWBASE, default src/image_write.c).  Output sorted to build/iw/subsets_<n>.txt; top 40 printed.
Score counts only functions it changes; the best per size is listed."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iwtricks

names = sys.argv[1:]
combos = [c for k in range(1, len(names) + 1) for c in itertools.combinations(names, k)]
print(len(combos), flush=True)
res = iwtricks.many(combos)
res = [(c, r) for c, r in res if 'compile' not in r]
res.sort(key=lambda x: (x[1]['total'], -len(x[0])))
out = os.path.join(iwlib.BUILD, 'subsets_%d.txt' % len(names))
with open(out, 'w', newline='\n') as f:
    for c, r in res:
        f.write('%s | %s\n' % (','.join(c), iwlib.fmt(r)))
for c, r in res[:40]:
    print(','.join(c), '|', iwlib.fmt(r)[:170])
print('best per size')
seen = set()
for c, r in res:
    if len(c) not in seen:
        seen.add(len(c))
        print(len(c), ','.join(c), '|', iwlib.fmt(r)[:170])
