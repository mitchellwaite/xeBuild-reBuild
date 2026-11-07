"""Attempt 56: follow the blocks holding a statement (default: the patch-size log) through every
tree dump of loadBlFiles: block -> successor, the successor's preds and first statements.
Dumps from a56_dump.py.  python tools/wip/dehint/bdgen/a56_trace.py <dumpdir> [text]"""
import sys,re,glob,os
d=sys.argv[1]; key=sys.argv[2] if len(sys.argv)>2 else 'patch size'
def fn(path):
    t=open(path,encoding='latin-1').read()
    i=t.find(';; Function loadBlFiles ')
    if i<0: return None
    j=t.find(';; Function ',i+10)
    return t[i:j if j>0 else None]
def blocks(t):
    B={};cur=None
    for l in t.split('\n'):
        m=re.match(r';;\s+basic block (\d+),',l)
        if m: cur=m.group(1); B[cur]=[]
        if cur: B[cur].append(l)
    return B
fs=sorted(glob.glob(os.path.join(d,'build.c.*t.*')),key=lambda p:int(re.search(r'\.(\d+)t\.',p).group(1)))
for f in fs:
    t=fn(f)
    if not t: continue
    B=blocks(t)
    sb=[k for k,v in B.items() if any(key in l for l in v)]
    if not sb: continue
    out=[]
    for k in sb:
        succ=[re.findall(r'(\d+) \[|(\d+) \(',l) for l in B[k] if 'succ:' in l]
        sl=[l for l in B[k] if 'succ:' in l]
        s=re.search(r'succ:\s+(\d+)',sl[0]).group(1) if sl else '?'
        sb2=B.get(s,[])
        preds=[re.search(r'(\d+)',l.split('pred:')[1] if 'pred:' in l else l).group(1) for l in sb2 if re.match(r';;\s+(pred:)?\s+\d+ ',l) or 'pred:' in l][:0]
        pl=[];inpred=False
        for l in sb2:
            if 'pred:' in l: inpred=True; l=l.split('pred:')[1]
            elif not re.match(r';;\s+\d+ \[',l): inpred=False
            if inpred:
                m=re.search(r'(\d+)',l); pl.append(m.group(1))
        stm=[l.strip() for l in sb2 if not l.startswith(';;') and l.strip()][:2]
        out.append('%s->%s preds=%s %s'%(k,s,','.join(pl),' | '.join(stm)[:110]))
    print(os.path.basename(f).split('.')[2], ' ; '.join(out))
