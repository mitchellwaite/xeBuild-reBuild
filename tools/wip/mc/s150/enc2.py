# enc2.py A.t B.t : compare jump targets by instruction index (ignoring alignment nops)
import re,sys
def load(f):
    r=[]
    for l in open(f):
        m=re.match(r'\s*([0-9a-f]+):\t([0-9a-f ]+)\t(.+)',l)
        if m: r.append((int(m.group(1),16),m.group(2).strip(),m.group(3).strip()))
    return r
isn=lambda x:re.match(r'(nop|xchg\s+ax,ax|lea\s+esi,\[esi)',x[2])
def prep(f):
    t=[x for x in load(f) if not isn(x)]
    idx={x[0]:i for i,x in enumerate(t)}
    return t,idx
A,ia=prep(sys.argv[1]);B,ib=prep(sys.argv[2])
for i,(x,y) in enumerate(zip(A,B)):
    mx=re.match(r'(j\w+)\s+([0-9a-f]+)',x[2]); my=re.match(r'(j\w+)\s+([0-9a-f]+)',y[2])
    bad=(x[1].split()[0]!=y[1].split()[0] or len(x[1].split())!=len(y[1].split()))
    if mx and my:
        ta=ia.get(int(mx.group(2),16)); tb=ib.get(int(my.group(2),16))
        if ta!=tb or mx.group(1)!=my.group(1): bad=True
    if bad: print(i,hex(x[0]),x[1],x[2][:28],'||',hex(y[0]),y[1],y[2][:28])
