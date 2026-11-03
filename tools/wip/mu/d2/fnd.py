"""fnd.py A B SUFFIX [FN]: print parseAddonIdx's dump of pass SUFFIX from dump dirs A and B into A.fn and B.fn (e.g. 123t.pre); diff with diff -u."""
import re,sys,os,glob
a,b,s=sys.argv[1:4]; fn=sys.argv[4] if len(sys.argv)>4 else 'parseAddonIdx'
for d in (a,b):
    p=glob.glob(d+'/m.c.'+s)[0]
    t=open(p,errors='replace').read()
    m=re.search(r';; Function '+fn+r'\b.*?(?=\n;; Function |\Z)',t,re.S)
    x=m.group(0)
    open(d+'.'+s+'.fn','w',newline='\n').write(x)
