import sys,os,re,glob
def cnt(d):
    r={}
    for f in sorted(glob.glob(os.path.join(d,'m.c.*'))):
        t=open(f,errors='ignore').read()
        i=t.find('\n;; Function mode_client')
        if i<0: continue
        j=t.find('\n;; Function',i+5); s=t[i:j if j>0 else None]
        n=len(set(re.findall(r'\n;; basic block (\d+)',s)) or set(re.findall(r'<bb (\d+)>',s)) or set(re.findall(r'\n\(code_label|\nbb (\d+)',s)))
        r[os.path.basename(f)[4:]]=(n,len(s))
    return r
a=cnt(sys.argv[1]);b=cnt(sys.argv[2])
for k in a:
    if k in b and a[k]!=b[k]: print(k,a[k],b[k])
