# gf.py BASE PFX : for every label reference (asm goto list entry or 'goto L;') inside mode_client/clientEraseBlockI,
# redirect that one reference to a forwarder zfN: asm volatile(""); goto L;  (defined after the final return 0)
import sys,re
base,pfx=sys.argv[1],sys.argv[2]
s=open(base).read()
a=s.find('static void clientEraseBlockI'); a2=s.find('char *getArgs'); b=s.find('int mode_client(int argc'); e=s.find('mc_rdpad')
refs=[]
for lo,hi in ((a,a2),(b,e)):
    for m in re.finditer(r'__asm__ goto \("" :::: ([^)]*)\)|JMP\(([^)]*)\)',s[lo:hi]):
        g=1 if m.group(1) is not None else 2
        st=lo+m.start(g)
        for mm in re.finditer(r'\w+',m.group(g)): refs.append((st+mm.start(),st+mm.end(),mm.group(0)))
    for m in re.finditer(r'goto (\w+);',s[lo:hi]):
        refs.append((lo+m.start(1),lo+m.end(1),m.group(1)))
ins=s.find('return 0;',s.find('connect to xbox server'))+len('return 0;')
for k,(i,j,L) in enumerate(refs):
    if L.startswith(('rk','fa','ork','ofa')) and not L.startswith(('rkE','rkn')) and k%3: continue
    t=s[:i]+'zf'+L+s[j:]
    t=t[:ins+2]+' zf%s: __asm__ volatile (""); goto %s;'%(L,L)+t[ins+2:] if ins>j else None
    n='%s%03d_%s'%(pfx,k,L); open(n+'.c','w',newline='\n').write(t); print(n)
