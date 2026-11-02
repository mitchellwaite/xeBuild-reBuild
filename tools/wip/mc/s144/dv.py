# dv.py : where do the shape2 c1 dummies pop, and does the solution survive if each dummy is instead
# absorbed (visited) by a later trace (no extra block in the layout)?
import sys
sys.path.insert(0, '.'); sys.argv = ['x', '../s143/dd/c1/mc.bbro']
exec(open('shape2.py').read().split('MOV =')[0])
sol = [('M', 128, 108, 1, 0), ('G', 69, 1, 0, 0), ('M', 79, 55, 4, 0), ('G', 143, 0, 0, 0), ('M', 81, 55, 5, 0)]
print('full', apply(sol)[i143-2:i143+20])
sol2 = [e for e in sol if e[0] == 'M']; print('moves only', score(apply(sol2)))
# dummies absorbed: insert dummy, visit it in group v
import itertools
def apply2(edits, vis):
    gg = {b: list(v) for b, v in g.items()}
    for ed in edits:
        if ed[0] == 'M':
            _, blk, to, at, k = ed
            for b in gg: gg[b] = [e for e in gg[b] if not (e[0] == 'ins' and e[2] == blk)]
            L = gg[to]; gg[to] = L[:at] + [('ins', 'this', blk, k)] + L[at:]
    for n, (to, at, k, v) in enumerate(vis):
        L = gg[to]; gg[to] = L[:at] + [('ins', 'this', DUM + n, k)] + L[at:]
        gg[v] = [('visit', DUM + n)] + gg[v]
    try: return r4sim.sim(pre, gg, {})
    except Exception: return []
o = apply(sol)
for v1 in o[o.index(69):o.index(69)+15]:
    for v2 in o[o.index(143):o.index(143)+15]:
        if v1 >= DUM or v2 >= DUM: continue
        oo = apply2(sol2, [(69, 1, 0, v1), (143, 0, 0, v2)])
        print(v1, v2, score(oo))
print('--- minimal subsets (dummy at 143 absorbed by 79)')
M = sol2
for r in range(len(M)+1):
    for sub in itertools.combinations(M, r):
        for d in [[], [(143, 0, 0, 79)], [(143, 0, -1, 79)]]:
            s = score(apply2(list(sub), d))
            if s <= 2: print(s, sub, d)
print('--- 128 source traces')
for to in o[:o.index(143)+1]:
    for at in range(len(g[to])+1):
        s = score(apply2([('M',128,to,at,0),('M',79,55,4,0),('M',81,55,5,0)], [(143,0,0,79)]))
        if s == 0: print('128 from', to, at)
