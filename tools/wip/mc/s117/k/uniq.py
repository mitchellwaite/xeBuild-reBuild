import sys,hashlib
R=sys.argv[1]; seen=set(); out=[]
for l in open(R+'/cost.txt'):
    p=l.split(); h=hashlib.md5(open(p[3]+'.mine','rb').read()).hexdigest()[:8]
    if h in seen: continue
    seen.add(h); out.append(h+' '+l.strip())
open(R+'/uniq.txt','w',newline='\n').write('\n'.join(out)+'\n')
print('\n'.join(out[:25]))
