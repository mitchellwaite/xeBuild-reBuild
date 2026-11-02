import json, sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 's23'))
import ext, table
base = [(44,'rok','pp'),(50,'rok','q')]
best = []
for a,b,c,d in itertools.product(range(0,4), [None,38,39,40,41], range(0,4), [None,42,43,44,45]):
  for nb in (1,2):
    inj = base + [(58,'rok','pp')]*a + ([(b,'rok','pp')]*nb if b else []) + [(59,'rok','pp')]*c + ([(d,'rok','pp')]*nb if d else [])
    try: r = table.meas(inj, 's24scan')
    except Exception as e: continue
    best.append((r['inv'], inj)); print(r['inv'], a,b,c,d,nb, r['fq'].get(110),r['fq'].get(111),r['fq'].get(112), flush=True)
best.sort(key=lambda x:x[0]); print(best[:5])
