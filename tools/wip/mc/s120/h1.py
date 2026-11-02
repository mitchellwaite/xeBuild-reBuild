import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s104')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import srch, r4sim
pre,g,first=r4sim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s118\dd\mc.bbro')
base=srch.sim(pre,g); want=srch.sim(pre,g,{152:1,75:1})
print('base',base); print('want',want)
def d(o):
    import difflib
    sm=difflib.SequenceMatcher(None,o,want,autojunk=False); return len(want)-sum(m.size for m in sm.get_matching_blocks())
pts=[('p',i) for i in range(len(pre)+1)]+[(b,j) for b in g for j in range(len(g[b])+1)]
print('npts',len(pts))
res=[]
for p in pts:
  for k in (-2,-1,0):
    o=srch.sim(pre,g,{},{p:k}); res.append((d(o),p,k))
res.sort(key=lambda r:r[0]); print(res[:15])
# removals: key -1 override of each key-0 node
rem=[]
for b in set(first):
  for k in (-1,-2,-3):
    o=srch.sim(pre,g,{b:k}); rem.append((d(o),b,k))
rem.sort(key=lambda r:r[0]); print('rem',rem[:10])
# pairs of dummies (key 0/-1) among top 200 singles plus removal combos
top=[r for r in res if r[0]<=d(base)][:250]
best=[]
for a,c in itertools.combinations(top,2):
  if a[1]==c[1]: continue
  o=srch.sim(pre,g,{},{a[1]:a[2],c[1]:c[2]}); best.append((d(o),a[1:],c[1:]))
best.sort(key=lambda r:r[0]); print('pairs',best[:10])
mix=[]
for a in top[:150]:
  for r in rem[:40]:
    o=srch.sim(pre,g,{r[1]:r[2]},{a[1]:a[2]}); mix.append((d(o),a[1:],r[1:]))
mix.sort(key=lambda r:r[0]); print('mix',mix[:10])
