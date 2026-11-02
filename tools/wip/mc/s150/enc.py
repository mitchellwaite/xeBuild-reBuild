# enc.py A.t B.t : instruction encoding differences ignoring addresses, listing nop-runs too
import re,sys
def load(f):
    r=[]
    for l in open(f):
        m=re.match(r'\s*([0-9a-f]+):\t([0-9a-f ]+)\t(.+)',l)
        if m: r.append((int(m.group(1),16),m.group(2).strip(),m.group(3).strip()))
    return r
a=load(sys.argv[1]); b=load(sys.argv[2])
isn=lambda x:re.match(r'(nop|xchg\s+ax,ax|lea\s+esi,\[esi)',x[2])
A=[x for x in a if not isn(x)];B=[x for x in b if not isn(x)]
print(len(A),len(B))
for i,(x,y) in enumerate(zip(A,B)):
    if x[1].split()[0]!=y[1].split()[0] or len(x[1].split())!=len(y[1].split()):
        print(i,hex(x[0]),x[1],x[2][:30],'||',hex(y[0]),y[1],y[2][:30])
for name,t in (('A',a),('B',b)):
    print(name,'nops at',[hex(x[0]) for x in t if isn(x) and x[0]>0x1f30][:40])
