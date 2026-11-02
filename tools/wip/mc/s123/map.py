# map.py : map best18 trace-time blocks (dd) to profiled (pf) by source construct
import difflib, sys
from cfg import parse
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
a = open(sys.argv[1] if len(sys.argv) > 1 else 'b18.c').read().split('\n')
b = open(R + r'\src\mode_client.c').read().split('\n')
lm = {}
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): lm[i1 + k + 1] = j1 + k + 1
last=0
for l in range(1,len(a)+2):
    if l in lm: last=lm[l]-l
    else: lm[l]=l+last
D, dd, dt = parse(sys.argv[2] if len(sys.argv) > 2 else 'dd')
P, pd, pt = parse('pf')
def sig(x, tr=None):
    ln = tuple(sorted(set((tr.get(l, -l) if tr else l) for l in x['ln'])))
    return (ln, tuple(sorted(x['sym'])))
ps = {}
for k, x in P.items():
    if k in pd: continue
    ps.setdefault(sig(x), []).append(k)
m = {}; used = set()
lived = [k for k in sorted(D) if k not in dd]
# pass 1: unique sig match
for k in lived:
    c = [p for p in ps.get(sig(D[k], lm), []) if p not in used]
    if len(c) == 1: m[k] = c[0]; used.add(c[0])
# pass 2: ambiguous: pick by freq closeness then CFG neighbour consistency
for it in range(3):
    for k in lived:
        if k in m: continue
        c = [p for p in ps.get(sig(D[k], lm), []) if p not in used]
        if not c: continue
        def score(p):
            s = 0
            for q in D[k]['pred']:
                if q[0].isdigit() and m.get(int(q[0])) is not None and any(r[0] == str(m[int(q[0])]) for r in P[p]['pred']): s += 10
            for q in D[k]['succ']:
                if q[0].isdigit() and m.get(int(q[0])) is not None and any(r[0] == str(m[int(q[0])]) for r in P[p]['succ']): s += 10
            return s - abs(P[p]['n'] - D[k]['n'])
        c.sort(key=score, reverse=True)
        if it == 2 or len(c) == 1 or score(c[0]) > score(c[1]): m[k] = c[0]; used.add(c[0])
# pass 3: same symbol set, nearest translated line
for k in lived:
    if k in m or not D[k]['sym']: continue
    tl = [lm.get(l, l) for l in D[k]['ln']] or [0]
    c = [p for p in P if p not in pd and p not in used and sorted(P[p]['sym']) == sorted(D[k]['sym'])]
    if c:
        c.sort(key=lambda p: min(abs(a - b) for a in tl for b in (P[p]['ln'] or [0])))
        m[k] = c[0]; used.add(c[0])
# pass 4: symless: same translated line set (+-3), neighbour consistent
for it in range(3):
  for k in lived:
    if k in m: continue
    tl = [lm.get(l, l) for l in D[k]['ln']]
    for p in P:
        if p in pd or p in used or P[p]['sym'] != D[k]['sym'] or not tl or not P[p]['ln']: continue
        if min(abs(a - b) for a in tl for b in P[p]['ln']) > 3: continue
        nb = sum(1 for q in D[k]['pred'] if q[0].isdigit() and str(m.get(int(q[0]))) in [r[0] for r in P[p]['pred']])
        if nb: m[k] = p; used.add(p); break
def fmt(x, t):
    return 'f%-5d n%-2d %-7s L%s %s' % (x['f'], x['n'], ('T%dr%d.%d' % t) if t else '-', ','.join(map(str, x['ln'][:4])), ' '.join(x['sym'][:2]))
print('== ours (best18) blocks with NO profiled counterpart:')
for k in lived:
    if k not in m:
        x = D[k]; print(' ', k, fmt(x, dt.get(k)), 'src', ','.join(str(lm.get(l, '?')) for l in x['ln'][:4]), 'p:' + ','.join(p[0] for p in x['pred']), 's:' + ','.join(s[0] for s in x['succ']))
print('== profiled blocks with NO best18 counterpart:')
for k in sorted(P):
    if k in pd or k in used: continue
    x = P[k]; print(' ', k, fmt(x, pt.get(k)), 'p:' + ','.join(p[0] for p in x['pred']), 's:' + ','.join(s[0] for s in x['succ']))
print('== mapped:', len(m))
with open('map.txt', 'w', newline='\n') as f:
    for k in sorted(m): f.write('%d %d | %s | %s\n' % (k, m[k], fmt(D[k], dt.get(k)), fmt(P[m[k]], pt.get(m[k]))))
