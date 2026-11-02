# gen.py OUTDIR BASE.c VARFILE : VARFILE lines "name|old|new[|old|new...]" ; old must occur once
import sys
out,base,vf=sys.argv[1:4]; T=open(base).read()
for ln in open(vf):
    ln=ln.rstrip('\n')
    if not ln or ln.startswith('#'): continue
    p=ln.split('~~'); nm=p[0]; s=T; ok=True
    for o,n in zip(p[1::2],p[2::2]):
        if s.count(o)!=1: print('BAD',nm,s.count(o),o); ok=False; break
        s=s.replace(o,n)
    if ok: open('%s/%s.c'%(out,nm),'w',newline='\n').write(s)
