# ext.py DUMP "[base changes]" : all 1-2 extra changes (real2 CH + key overrides on tail blocks) on top of base
import sys,ast,importlib.util as u
sp=u.spec_from_file_location('real2',r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s150\real2.py'); m=u.module_from_spec(sp); sp.loader.exec_module(m)
m.init(sys.argv[1]); base=ast.literal_eval(sys.argv[2]); CH=list(m.CH)
KO=[('key',b,k) for b in (147,150,128,75,79,81,35,42,53,144) for k in (-1,-2)]
def run(cs):
    gg=dict(m.g); ins=[c for c in cs if c[0]!='key']; ov={c[1]:c[2] for c in cs if c[0]=='key'}
    for n,c in sorted(enumerate(ins),key=lambda x:(-x[1][2],x[0])):
        L=list(gg[c[1]]); L.insert(c[2],('ins','this',m.D+1+n,c[3]) if c[0]=='dum' else ('ins','this',c[3],m.KEY[c[3]])); gg[c[1]]=L
    try: return m.sc(m.r4sim.sim(m.pre,gg,ov))
    except Exception: return 99
print('base',run(base))
S=sorted((run(base+[c]),c) for c in CH+KO); print(S[:10])
for s,c in S:
    if s==0: print('SOL1',c)
top=[c for s,c in S if s<=4][:150]; print(len(top)); n=0
for a in top:
    for b in CH+KO:
        if run(base+[a,b])==0:
            n+=1
            if n<60: print('SOL2',a,b)
print('nsol2',n)
