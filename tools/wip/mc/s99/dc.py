# dc.py BASE OUT c1,c2,..,c12,cdef : set number of dsp asm-gotos before 'break;' of each case in the dispatch switch
import sys,re
b,o,cs=sys.argv[1:4]; cs=list(map(int,cs.split(',')))
L=open(b).read().split('\n')
d0=[i for i,l in enumerate(L) if 'dsp: cinfo' in l][0]; st=[i for i,l in enumerate(L) if i>d0 and l.strip()=='case 1:'][0]
G='__asm__ goto ("" :::: dsp); '
cases=['case %d:'%i for i in range(1,13) if i!=6]+['default:']
pos=[i for i in range(st,st+60) if L[i].strip() in cases]
assert len(pos)==12,len(pos)
for j,p in enumerate(pos):
    q=p+1
    while not L[q].rstrip().endswith('break;'): q+=1
    l=L[q]; ind=l[:len(l)-len(l.lstrip())]; body=l.strip().replace(G.strip(),'').strip()
    body=re.sub(r'^\s*','',body)
    L[q]=ind+G*cs[j]+body
open(o,'w',newline='\n').write('\n'.join(L))
