import sys,itertools
f=sys.argv[1]; sys.argv=['x',f,'0','0']
exec(open('wr2.py').read().split('random.seed')[0])
res=[]
bl=[b for b in T[4:]]+[142,105,123]
for b in bl:
  for k in range(-5,2):
    try: o=r4sim.sim(pre,g,{b:k}); res.append((score([x for x in o if x<900]),b,k))
    except Exception as e: pass
for b1,b2 in itertools.combinations(bl,2):
  for k1 in range(-4,1):
    for k2 in range(-4,1):
      try: o=r4sim.sim(pre,g,{b1:k1,b2:k2}); res.append((score([x for x in o if x<900]),b1,k1,b2,k2))
      except Exception: pass
res.sort(); print(res[:30])
