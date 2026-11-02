import sys,difflib,re
n=sys.argv[1]
da=[l.strip() for l in open('dd/%s/mc.da'%n)]
ins=[];cur=None
for l in da:
    m=re.match(r'# BLOCK (\d+)',l)
    if m: cur=int(m.group(1)); continue
    if l.startswith('#') or l.endswith(':') or l.startswith('.'): continue
    ins.append((cur,l.split()[0]))
mine=[l.rstrip('\n') for l in open('v/%s.mine'%n)]
ref=[l.rstrip('\n') for l in open('v/%s.ref'%n)]
a=[x[1] for x in ins]; b=[l.split()[0] if l.split() else '' for l in mine]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
mb={}
for i,j,k in sm.get_matching_blocks():
    for t in range(k): mb[j+t]=ins[i+t][0]
# mine line -> block; ref line -> via diff with mine
sm2=difflib.SequenceMatcher(None,ref,mine,autojunk=False)
rb={}
for i,j,k in sm2.get_matching_blocks():
    for t in range(k): rb[i+t]=mb.get(j+t)
lo,hi=int(sys.argv[2]),int(sys.argv[3])
print('MINE');prev=None;o=[]
for j in range(lo,hi):
    if mb.get(j)!=prev: prev=mb.get(j); o.append(prev)
print(o)
print('REF');prev=None;o=[]
for i in range(lo,hi):
    x=rb.get(i,'?')
    if x!=prev: prev=x; o.append(x)
print(o)
import re as _r
t=open('dd/%s/mc.bbro'%n).read(); i=t.index('Reordered sequence:')
seq=[int(b) for a,b in _r.findall(r'^ *(\d+) bb (\d+) ',t[i:i+20000],_r.M)]
for j in range(lo,hi): print(j+1, seq[mb[j]] if mb.get(j) is not None else '?', mine[j])
