# nonin.py N : top-N distinct (by asm hash) non-inert singles -> nonin.json
import json, sys, gen
S = json.load(open('singles.json'))

base = gen.evaluate([])
C = gen.load_cache()
_, _, bh = C[gen.key([])]
seen = {bh}; out = []
for r, e in S:
    if r[0] >= 9999: continue
    h = C.get(gen.key([tuple(e)]), [0, 0, None])[2]
    if h in seen or tuple(r) == tuple(base): continue
    seen.add(h); out.append([r, e])
json.dump(out[:int(sys.argv[1])], open('nonin.json', 'w'))
print(len(out), out[:5])
