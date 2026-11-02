"""tr2.py TAG [rN]: traces with labels (Final order positional mapping); ref-role position of each trace head"""
import sys,re,lab
D='../../../../build/v/aio_p1/%s/'%sys.argv[1]
labs,ids=lab.our_blocks(D+'o.s')
t=open(D+'aio.bbro').read()
fo=t[t.index('Final order:'):].split('\n')[1].split()
if len(fo)!=len(labs): print('LEN',len(fo),len(labs))
L=dict(zip(fo,labs))
o=lab.orig_blocks()
pos={}
for i,x in enumerate(o): pos.setdefault(x,i)
want=sys.argv[2] if len(sys.argv)>2 else None
for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$',t,re.M):
    if want and 'r'+m.group(2)!=want: continue
    bbs=re.findall(r'(\d+) \[(\d+)\]',m.group(3))
    print('T%-3s r%s %4s '%(m.group(1),m.group(2),pos.get(L.get(bbs[0][0],'?'),'?')),' '.join('%s[%s]%s'%(b,f,L.get(b,'?').split('/')[0].replace('-:.','.')) for b,f in bbs))
