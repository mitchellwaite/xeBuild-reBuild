import sys
from tmap import target
n=sys.argv[1]
T,m=target(n+'.c','d/%s/order.txt'%n)
names=['inv','-ip','hdd5','hdd4','u2','-r','Blk','Fer','-w','wb4','wb3','-e','Inv','Pat','Info','wb5','eb5','ip3','c3','c5','-c']
rev={b:nm for nm,b in m.items()}
pos={b:i for i,b in enumerate(T)}; seen=[]
for l in open('d/%s/order.txt'%n):
    p=l.split()
    if len(p)>2 and p[1]=='old' and p[2].isdigit() and int(p[2]) in pos and int(p[2]) not in seen: seen.append(int(p[2]))
print(' '.join(names[pos[b]]+':'+str(b) for b in seen))
