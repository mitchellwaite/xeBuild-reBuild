import sys,json;sys.path.insert(0,'../s86');import r4sim
def K(d):
    pre,g,f=r4sim.load(d);k={}
    for e in pre:
        if e[0]=='push': k[e[1]]=e[2]
        if e[0]=='ins' and e[1]!='this': k[e[2]]=e[3]
        if e[0]=='chg' and e[1] in k: k[e[1]]=e[2]
    for v in g.values():
        for e in v:
            if e[0]=='ins': k.setdefault(e[2],e[3])
    return k,f
kp,fp=K('../s111/pf/mc.bbro'); kv,fv=K('dd/vEa/mc.bbro')
pm=dict(zip("133 94 109 111 112 115 110 122 123 124 132 118 136 49 117 114 104 55 129 128 61 33 29 67 131 119 134 35 42 53 77 79 73 81 86 140 95 141 96 91 93".split(),"147 96 113 117 120 123 116 131 132 139 146 134 152 49 127 122 108 55 144 143 62 33 29 69 145 129 150 35 42 53 81 79 75 83 88 160 97 161 98 93 95".split()))
def dec(k):
    if k is None: return '-'
    if k<=-1000000: return f"p{(-k-1000000)//100}/f{(-k-1000000)%100}"
    return f"f{-k}"
for p in fp:
    v=int(pm[str(p)]); print(f"P{p:>4} {dec(kp.get(p)):>10}  V{v:>4} {dec(kv.get(v)):>10}")
ov={}
for p in fp:
    v=int(pm[str(p)])
    if p in kp: ov[v]=kp[p]
pre,g,f=r4sim.load('dd/vEa/mc.bbro')
o=r4sim.sim(pre,g,ov); print(' '.join(map(str,o)))
T=[int(pm[str(p)]) for p in fp]; print(' '.join(map(str,T)))
sys.argv=['x'];
