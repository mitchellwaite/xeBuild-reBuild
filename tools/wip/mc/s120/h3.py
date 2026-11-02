exec(open('h1.py').read().split("print('npts'")[0])
import copy,time
ins=[(b,j,e) for b in g for j,e in enumerate(g[b]) if e[0]=='ins']
print('ins events',len(ins))
def mv(G,b,j,nb,nj):
  G=copy.deepcopy(G); e=G[b].pop(j); G.setdefault(nb,[]); G[nb].insert(nj,e); return G
moves=[]
for b,j,e in ins:
  for nb in g:
    for nj in range(len(g[nb])+1):
      if nb==b and nj in (j,j+1): continue
      moves.append((b,j,nb,nj))
print('moves',len(moves))
hits=[];sc=[]
for m in moves:
  G=mv(g,*m); o=srch.sim(pre,G); dd=d(o)
  if dd==0: hits.append(m)
  if o!=base: sc.append((dd,m))
print('single move hits',hits)
sc.sort(); print(sc[:10], len(sc))
# moves that preserve everything except changing structure (d<=1 and o==base): keep as neutral for pairing
neutral=[m for m in moves if srch.sim(pre,mv(g,*m))==base]
print('neutral',len(neutral))
t=time.time(); h2=[]
for m in neutral:
  G=mv(g,*m)
  for b2,j2,e2 in [(b,j,e) for b in G for j,e in enumerate(G[b]) if e[0]=='ins' and e[2] in (152,75,83)]:
    for nb in G:
      for nj in range(len(G[nb])+1):
        o=srch.sim(pre,mv(G,b2,j2,nb,nj))
        if d(o)==0: h2.append((m,(b2,j2,nb,nj)))
print('pair hits',len(h2),h2[:20],time.time()-t)
