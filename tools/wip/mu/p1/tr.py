"""tr.py DIR [-a]: DIR holds m.c.*bbro + m.s of a compile. Traces of mode_update (round, bb[freq], name). Names from the pre-reorder RTL."""
import re,sys,glob
d=sys.argv[1]
s=open(glob.glob(d+'/*bbro')[0]).read()
s=s[s.index(';; Function mode_update'):]
asm=open(d+'/m.s').read()
lc={}
for m in re.finditer(r'^(LC\d+):\n\s+\.ascii "(.*)"$',asm,re.M): lc[m.group(1)]=m.group(2)
i0=s.index('Reordered sequence:'); i1=s.rindex('Reordered sequence:')
parts=re.split(r'^\(note \d+ \d+ \d+ \d+ \[bb (\d+)\] NOTE_INSN_BASIC_BLOCK\)',s[i0:i1],flags=re.M)
nm={}
mp={}
for m in re.finditer(r'^ (\d+) (?:bb (\d+)|duplicate of (\d+))  \[(\d+)\]$',s[i0:i1],re.M):
    mp[int(m.group(1))]=(int(m.group(2) or m.group(3)),m.group(3) is not None)
for k in range(1,len(parts),2):
    b=mp[int(parts[k])]; t=parts[k+1]
    if b[1]: continue
    b=b[0]
    ss=[lc.get(x,x) for x in re.findall(r'symbol_ref/f:SI \("\*(LC\d+)"',t)]
    cs=re.findall(r'symbol_ref:SI \("(\w+)"\) \[flags 0x41\]',t)
    nm[b]=(ss[0].replace('\12','').replace('\0','')[:30] if ss else ''),(','.join(cs)[:24])
def N(b):
    a,c=nm.get(b,('',''))
    return a or c or '.'
if __name__=='__main__':
    tr=re.findall(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$',s,re.M)
    for n,r,body in tr:
        bs=re.findall(r'(\d+) \[(\d+)\]',body)
        if len(sys.argv)>2 or int(r)>=3:
            print('T%s r%s'%(n,r),' '.join('%s[%s]{%s}'%(x[0],x[1],N(int(x[0]))) for x in bs)[:300])
    print(re.search(r'Final order:\n(.*)',s).group(1))
