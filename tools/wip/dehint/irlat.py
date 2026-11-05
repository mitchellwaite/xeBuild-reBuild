"""python tools/wip/dehint/irlat.py <sweep output>: rank a hint lattice's labels by hint count, then lines.
Prints the best line count for each number of hints (labels as in gen_ir129/130)."""
import re, sys
HINT = {'vh': 1, 'bh': 1, 'sh': 1, 'un': 1, 'ex': 1, 'noa': 1, 'k3': 1, 'tm': 1, 'i2': 1, 'tmi': 1, 'i1': 1, 'i12': 1, 'i1m': 1, 'a3': 1}
rows = []
for l in open(sys.argv[1]):
    m = re.match(r'(\d+) \| ([^|]+) \|', l)
    if not m:
        continue
    lab = m.group(2).strip()
    n = sum(HINT.get(p, 0) for p in lab.split('.'))
    rows.append((n, int(m.group(1)), lab))
rows.sort()
seen = {}
for n, k, lab in rows:
    seen.setdefault(n, [])
    if len(seen[n]) < 6:
        seen[n].append((k, lab))
for n in sorted(seen):
    print(n, 'hints:', ' '.join('%d:%s' % x for x in seen[n]))
print('below 7 hints and 0 lines:', [r for r in rows if r[1] == 0 and r[0] < 7])
