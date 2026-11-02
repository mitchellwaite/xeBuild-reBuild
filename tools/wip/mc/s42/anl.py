import json, sys, collections
B = ['2:1038:ins/next/53', '3:53:push/53/0', '4:55:ins/this/77', '4:55:ins/this/79']
def norm(s): return [x for x in s]
rs = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
ok = [r for r in rs if 'inv' in r]
print('n', len(rs), 'ok', len(ok), 'min inv', min(r['inv'] + 5 * len(r['miss']) for r in ok))
C = collections.Counter()
mv = []
for r in ok:
    s = r['sig']
    k = tuple(x for x in s if not x.startswith('2:1038') and not x.startswith('2:1039') and not x.startswith('2:104'))
    # moved = 53 not inserted by round-2 loop trace, or 77/79 not at 55
    m53 = not any(x.endswith('ins/next/53') and x.startswith('2:') for x in s)
    m77 = '4:55:ins/this/77' not in s; m79 = '4:55:ins/this/79' not in s
    if m53 or m77 or m79: mv.append((r['inv'] + 5 * len(r['miss']), r['c'], s))
    C[tuple(s)] += 1
print('moved', len(mv))
for x in sorted(mv)[:40]: print(x)
for s, n in C.most_common(12): print(n, s)
