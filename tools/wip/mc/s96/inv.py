import sys
from tmap import target
n=sys.argv[1]
try: T,_=target(n+'.c','d/%s/order.txt'%n)
except Exception as e: print('inv?'); sys.exit()
pos={b:i for i,b in enumerate(T)}; seen=[]
for l in open('d/%s/order.txt'%n):
    p=l.split()
    if len(p)>2 and p[1]=='old' and p[2].isdigit() and int(p[2]) in pos and int(p[2]) not in seen: seen.append(int(p[2]))
q=[pos[b] for b in seen]
print('inv=%d'%sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j]))
