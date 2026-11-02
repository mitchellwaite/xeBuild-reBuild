import sys,itertools
f=sys.argv[1]; sys.argv=['x',f,'0','0']
exec(open('wr2.py').read().split('random.seed')[0])
base=score(r4sim.sim(pre,g,{}))
print('base',base, [ (b,[e for e in g[b] if e[0]=='ins']) for b in first[:8]])
for b in first:
  ins=[e for e in g[b] if e[0]=='ins']
  if len(ins)<2: continue
  oth=[e for e in g[b] if e[0]!='ins']
  for p in itertools.permutations(ins):
    gg=dict(g); gg[b]=oth+list(p)
    try: s=score(r4sim.sim(pre,gg,{}))
    except Exception as e: continue
    if s<base: print(b,s,[e[2] for e in p])
