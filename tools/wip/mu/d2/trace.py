"""trace.py DIR PATTERN [from_pass]: for each tree pass print lines of parseAddonIdx matching PATTERN (regex) with the pass name when they change."""
import re,sys,glob,os
d,pat=sys.argv[1:3]
last=None
for p in sorted(glob.glob(d+'/m.c.*t.*'),key=lambda x:int(re.search(r'm\.c\.(\d+)',x).group(1))):
    t=open(p,errors='replace').read()
    m=re.search(r';; Function parseAddonIdx\b.*?(?=\n;; Function |\Z)',t,re.S)
    if not m: continue
    body=m.group(0)
    i=body.find('\nparseAddonIdx (')
    if i<0: continue
    ls=[l for l in body[i:].split('\n') if re.search(pat,l)]
    k='\n'.join(ls)
    if k!=last:
        print('---',os.path.basename(p)[4:]); print(k); last=k
