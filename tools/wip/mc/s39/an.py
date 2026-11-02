import json, sys
J1 = '129 107 109 110 108 119 120 121 128 113 116 132 49 115 112 103 55 125 126 61 33 29 67 127 117 130 35 42 53 79 77'.split()
rows = [json.loads(l) for l in open(sys.argv[1])]
def bef(o, a, b): return o.index(a) < o.index(b) if a in o and b in o else None
cnt = {}
for r in rows:
    o = list(map(str, r['o']))
    k = (bef(o,'113','108'), bef(o,'126','125'), bef(o,'77','79'))
    r['k'] = k
    cnt.setdefault(k, []).append(r)
for k, v in sorted(cnt.items(), key=lambda z: str(z[0])):
    v.sort(key=lambda r: (r['s'], r['f']))
    print(k, len(v), 'best', v[0]['s'], v[0]['f'])
    for r in v[:int(sys.argv[2]) if len(sys.argv)>2 else 3]:
        c = r['c']; print('   ', r['s'], r['f'], c['v'][-1:], c['a'][-1:], c['e'][-1:], ' '.join(map(str, r['o'][:31])))
