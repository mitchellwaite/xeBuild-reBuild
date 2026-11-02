import sys,itertools
out,base,vf=sys.argv[1:4]; T=open(base).read()
V=[]
for ln in open(vf):
    ln=ln.rstrip('\n')
    if ln and not ln.startswith('#'):
        p=ln.split('~~'); V.append((p[0],list(zip(p[1::2],p[2::2]))))
def app(s,eds):
    for o,n in eds:
        if s.count(o)!=1: return None
        s=s.replace(o,n)
    return s
n=0
for (a,ea),(b,eb) in itertools.combinations(V,2):
    s=app(T,ea+eb)
    if s: open('%s/%s+%s.c'%(out,a,b),'w',newline='\n').write(s); n+=1
print(n)
