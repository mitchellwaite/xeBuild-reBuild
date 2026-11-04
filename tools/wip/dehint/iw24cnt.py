import re,sys,glob
d,fn,pat=sys.argv[1:4]
for f in sorted(glob.glob(d+'/a.c.*t.*')):
    tx=open(f,errors='replace').read()
    m=re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)'%fn,tx,re.S|re.M)
    if not m: continue
    n=[l for l in m.group(0).split('\n') if re.search(pat,l) and '# ' not in l[:6]]
    print(f.split('a.c.')[1],len(n),' | '.join(x.strip() for x in n[:4])[:150])
