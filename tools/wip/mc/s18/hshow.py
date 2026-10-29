import json,sys
sys.path.insert(0,'.')
import hsim
R,keys=hsim.load(sys.argv[1])
l=[x for x in open(sys.argv[2]) if x.split(' ')[0].isdigit()][-1]
d=json.loads(l.split(' ',2)[2])
f={int(k):v for k,v in d['f'].items()}; P={int(k):v for k,v in d['P'].items()}
if P.get(125): P[125]=(f[126]+1)//2
o=hsim.sim(R,f,P); print(hsim.inv(o)); print(' '.join(map(str,o)))
print(' '.join('%d:%d/%d'%(b,P.get(b,0),f[b]) for b in o if b in f))
