import subprocess,sys,re,random
# gr2.py BASE.c OUTPREFIX [secs] : first-improvement hill climb over bcp-goto chain edits + cold/hot labels
src0=open(sys.argv[1]).read(); out=sys.argv[2]
import time; T=time.time()+float(sys.argv[3]) if len(sys.argv)>3 else 1e18
BCP=re.compile(r'if \(((?:\(char \*\))?__builtin_constant_p\((\w+) \+ (\d+)\)(?: == (?:\(char \*\))?\d+)?(?: && (?:\(char \*\))?__builtin_constant_p\(\w+ \+ \d+\)(?: == (?:\(char \*\))?\d+)?)*)\) (goto \w+|mode = \d+);')
def cands(src):
    C=[]
    for m in BCP.finditer(src):
        s=m.group(0); chain=m.group(1); var=m.group(2); act=m.group(4)
        if 'mode + 260' in s: continue
        parts=chain.split(' && ')
        C.append(('del',m.start(),s,''))
        n=int(re.findall(r'\+ (\d+)\)',parts[-1])[0])
        C.append(('add',m.start(),s,'if (%s && __builtin_constant_p(%s + %d)) %s;'%(chain,var,n+50000,act)))
        if len(parts)>1:
            C.append(('rm',m.start(),s,'if (%s) %s;'%(' && '.join(parts[:-1]),act)))
    for lab in re.findall(r'AT\((\w+)\) ',src):
        for k in ('cold','hot'):
            C.append(('lab',src.index('AT(%s) '%lab),'AT(%s) '%lab,'AT(%s) { %s_%s: __attribute__((%s)); } '%(lab,lab,k[0],k)))
    return C
def score(s):
    p='v/%s_t.c'%out
    open(p,'w',newline='\n').write(s)
    r=subprocess.run(['sh','f.sh',p],capture_output=True,text=True)
    try: return int(r.stdout.strip())
    except: return 9999
cur=src0; cs=score(cur); print('base',cs,flush=True)
log=open('%s.log'%out,'a')
rnd=0
while time.time()<T:
    C=cands(cur); random.shuffle(C); imp=False
    for kind,pos,o,n in C:
        if time.time()>T: break
        if cur[pos:pos+len(o)]!=o: continue
        s=cur[:pos]+n+cur[pos+len(o):]
        sc=score(s); log.write('%d %s %d %s\n'%(rnd,kind,sc,n[:100])); log.flush()
        if sc<cs or (sc==cs and random.random()<0.5 and kind!='lab'):
            imp=imp or sc<cs; cur,cs=s,sc; print('accept',kind,sc,n[:100],flush=True)
            open('%s_best.c'%out,'w',newline='\n').write(cur)
            break
    rnd+=1
    if not imp and rnd>400: break
print('final',cs)
