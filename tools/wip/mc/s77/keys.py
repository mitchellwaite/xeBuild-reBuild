import re,sys
# keys.py mc.bbro : last key per bb before round 4 + label from order.txt
L=open(sys.argv[1]).read().split('\n'); lab={}
for l in open(sys.argv[2]):
    p=l.split(); lab[p[2]]=' '.join(x for x in p[6:] if not x.startswith('L') or not x[1:].isdigit())[:40]
key={}
for l in L:
    if l.startswith('STC - round 4'): break
    m=re.search(r'(?:Changing key for bb (\d+) from \S+ to (\S+)\.|start[^:]*: (\d+) \(key: (\S+)\))',l)
    if m:
        if m.group(1): key[m.group(1)]=m.group(2)
        else: key[m.group(3)]=m.group(4)
r4=[];on=False
for l in L:
    if l.startswith('STC - round 4'): on=True
    if on:
        m=re.match(r'Getting bb (\d+)',l)
        if m: r4.append(m.group(1))
    if l.startswith('Trace 1 '): break
for b in r4: print(b,key.get(b,'?'),lab.get(b,''))
