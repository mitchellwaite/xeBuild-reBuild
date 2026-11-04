import sys,re,ast,collections
f=sys.argv[1]
rows=[]
for l in open(f):
    m=re.match(r'(\d+) gen(\d+) (\S*) (\{.*\})',l)
    if not m: continue
    rows.append((int(m.group(1)),int(m.group(2)),m.group(3),ast.literal_eval(m.group(4))))
print(len(rows))
for fn,lim in (('_imgAdd',5),('_imgAddFile',19),('_writeFsTable',5),('_imgAdd.constprop.1',0),('_imgAdd.constprop.4',0)):
    b=sorted([r for r in rows if r[3].get(fn,0)<=lim and r[0]<200],key=lambda r:r[0])
    print(fn,len(b),[(r[0],r[1],r[2],{k[1:]:v for k,v in r[3].items()}) for r in b[:6]])
