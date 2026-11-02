import sys; sys.path.insert(0,'../s123')
from cfg import parse
r=parse(sys.argv[1]); B=r[0] if isinstance(r,tuple) else r
for b in map(int,sys.argv[2:]):
  x=B[b]; print(b,'f',x['f'],'succ',[(s,p) for s,p,_ in x['succ']],'pred',[(s,p) for s,p,_ in x['pred']],'ln',x['ln'][:4],x['sym'][:3])
