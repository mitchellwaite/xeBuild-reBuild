"""fq.py C TAG: compile with -fdump-rtl-compgotos-blocks-details, print bb freq + succ edge probs (raw ids)."""
import os,sys,subprocess,re
ROOT=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'; BIN=os.path.join(ROOT,'tools','toolchain-4745','mingw32','bin')
FL=['-O3','-fno-toplevel-reorder','-fno-ipa-profile','-fno-reorder-functions','--param','builtin-expect-probability=50']
def fq(text,tag):
    sd=os.path.join(ROOT,'build','v','s54fq_'+tag); os.makedirs(sd,exist_ok=True)
    open(os.path.join(sd,'m.c'),'w',newline='\n').write(text)
    env=dict(os.environ,PATH=BIN+os.pathsep+os.environ['PATH'])
    subprocess.run([os.path.join(BIN,'gcc.exe'),'-S']+FL+['-I'+os.path.join(ROOT,'src'),'-fdump-rtl-compgotos-blocks-details','m.c','-o','o.s'],cwd=sd,env=env,check=True)
    t=open(os.path.join(sd,'m.c.267r.compgotos')).read()
    t=t[t.find('Function mode_client'):]
    bbs={}
    for m in re.finditer(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)',t): bbs[int(m.group(1))]={'f':int(m.group(2))}
    for m in re.finditer(r';; basic block (\d+),.*?\n(.*?);;  succ:(.*?)\n(?!;;\s{8,})',t,re.S): pass
    return bbs,t
if __name__=='__main__':
    b,t=fq(open(sys.argv[1]).read(),sys.argv[2])
    print(len(b)); i=t.find(';; basic block'); print(t[i:i+600])
def parse(t):
    out={}
    for blk in re.split(r'\n(?=;; basic block )',t)[1:]:
        m=re.match(r';; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)',blk)
        if not m: continue
        s=re.search(r';;  succ:(.*?)\n(?!;;\s{6,}\d)',blk,re.S)
        su=re.findall(r'(\d+|EXIT) \[([\d.]+)%\]',s.group(1)) if s else []
        p=re.search(r';;  pred:(.*?)\n(?!;;\s{6,}\d)',blk,re.S)
        pr=re.findall(r'(\d+|ENTRY) \[([\d.]+)%\]',p.group(1)) if p else []
        out[int(m.group(1))]=(int(m.group(3)),su,pr,int(m.group(2)))
    return out
def show(path,tag,lo,hi):
    b,t=fq(open(path).read() if path.endswith('.c') else path,tag); P=parse(t)
    for k in range(lo,hi+1):
        if k in P: print(k,'f',P[k][0],'d',P[k][3],'succ',' '.join('%s:%s'%x for x in P[k][1]),'| pred',' '.join('%s:%s'%x for x in P[k][2]))
def calls(t):
    out={}
    for blk in re.split(r'\n(?=;; basic block )',t)[1:]:
        m=re.match(r';; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)',blk)
        if m:
            for s in set(re.findall(r'symbol_ref:SI \("(\w+)"\)',blk)): out.setdefault(s,[]).append((int(m.group(1)),int(m.group(3))))
    return out
