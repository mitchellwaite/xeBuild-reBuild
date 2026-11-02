# lp.py BASE OUT SUBSTR K perm : permute labels of the K-th asm goto list on the unique line containing SUBSTR
import sys,re
b,o,sub,K,pm=sys.argv[1:6]; K=int(K)
L=open(b).read().split('\n')
k=[i for i,l in enumerate(L) if sub in l]; assert len(k)==1,len(k); k=k[0]
ms=list(re.finditer(r'goto \(""\s*::::\s*([^)]*)\)',L[k])); m=ms[K]
labs=[x.strip() for x in m.group(1).split(',')]; n=len(labs)
if pm=='rev': idx=list(range(n))[::-1]
else: idx=list(map(int,pm.split(',')))
assert sorted(idx)==list(range(n))
L[k]=L[k][:m.start(1)]+', '.join(labs[i] for i in idx)+L[k][m.end(1):]
open(o,'w',newline='\n').write('\n'.join(L)); print(n,file=sys.stderr)
