"""pe.py TAG FUNC: compact profile_estimate CFG of FUNC"""
import re,sys,glob
f=glob.glob('../../../../build/v/aio_p1/%s/a.c.*profile_estimate'%sys.argv[1])[0]
t=open(f).read()
ms=[m.start() for m in re.finditer(r'^;; Function %s '%sys.argv[2],t,re.M)]
i=ms[-1]; j=t.find('\n;; Function',i+10); s=t[i:j]
for m in re.finditer(r'^;; basic block (\d+), loop depth \d+, count \d+, freq (\d+)[^\n]*\n;;  prev[^\n]*\n((?:;;  pred:[^\n]*\n(?:;;   {5,}[^\n]*\n)*)?)((?:;;  succ:[^\n]*\n(?:;;   {5,}[^\n]*\n)*)?)',s,re.M):
    su=re.findall(r'(\d+|EXIT) \[([\d.]+)%\]',m.group(4))
    print('bb%s f%s -> %s'%(m.group(1),m.group(2),' '.join('%s:%s'%x for x in su)))
