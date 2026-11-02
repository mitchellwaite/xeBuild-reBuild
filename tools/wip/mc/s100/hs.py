# hs.py NAME : hot signature (r1-3 blocks in final order: trace round, freq, labels)
import sys,re
o=[]
for l in open('d/%s/order.txt'%sys.argv[1]):
    p=l.split()
    if len(p)<6: continue
    m=re.match(r'T\d+r(\d)',p[3])
    if not m or m.group(1)=='4': continue
    o.append(m.group(1)+':'+p[5]+':'+','.join(x for x in p[6:]))
print('\n'.join(o))
