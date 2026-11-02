# pf.py BASE OUT LINE_PREFIX perm(comma idx list, or 'rev', or 'rot:k') : permute dead-goto ifs on the line starting with prefix
import sys,re
b,o,pre,pm=sys.argv[1:5]
L=open(b).read().split('\n')
k=[i for i,l in enumerate(L) if l.lstrip().startswith(pre)]; assert len(k)==1,len(k); k=k[0]
l=L[k]; h=l.index('if (')
head,body=l[:h],l[h:]
parts=[p.strip() for p in re.split(r'(?<=;)\s+(?=if \()',body)]
n=len(parts)
if pm=='rev': idx=list(range(n))[::-1]
elif pm.startswith('rot:'): r=int(pm[4:]); idx=[(i+r)%n for i in range(n)]
elif pm.startswith('sw:'): a,c=map(int,pm[3:].split('-')); idx=list(range(n)); idx[a],idx[c]=idx[c],idx[a]
else: idx=list(map(int,pm.split(',')))
assert sorted(idx)==list(range(n)),(n,idx)
L[k]=head+' '.join(parts[i] for i in idx)
open(o,'w',newline='\n').write('\n'.join(L))
print(n,file=sys.stderr)
