# fq.py NAME... : freq + bb of window blocks identified by source line
import sys,re
T=[('u2','client_usage(2, NULL)',0),('i0','clientInfo(NULL)',0),('p0','clientPatches(NULL)',0),
   ('einv','provide hex only for offset!',1),('efail','Failed to erase block',0),('eout','is outside system area',0)]
for d in sys.argv[1:]:
    src=open('dd/%s/pm.c'%d).read().split('\n')
    t=open('dd/%s/mc.bbro'%d).read(); i=t.index('Reordered sequence:')
    f={a:(b,c) for a,b,c in re.findall(r'^ *(\d+) bb (\d+) +\[(\d+)\]',t[i:i+20000],re.M)}
    body=t[t.index('\n(',i):]
    l2b={}
    for ins in re.split(r'\n(?=\()',body):
        m=re.match(r'\(call_insn\S* \d+ \d+ \d+ (\d+) ',ins)
        if m:
            for l in re.findall(r'pm\.c:(\d+)',ins): l2b.setdefault(int(l),set()).add(m.group(1))
    out=[]
    for n,s,k in T:
        ls=[j+1 for j,x in enumerate(src) if s in x]; ln=ls[k] if len(ls)>k else ls[-1]
        bs=sorted(l2b.get(ln,()),key=int)
        out.append('%s=%s'%(n,'/'.join('%s:%s'%f.get(b,(b,'?')) for b in bs) or '-'))
    print(' '.join(out))
