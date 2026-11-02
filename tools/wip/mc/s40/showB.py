import json,sys,ev
rows=[]
for l in open(sys.argv[1]):
    t,e,r=json.loads(l)
    if 'order' not in r: continue
    inv,miss,o=ev.score_order(r['order'].split()[1:])
    rows.append((inv+5*len(miss),r['fncmp'],t,e,' '.join(map(str,o))))
rows.sort()
for x in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 15]: print(x[0],x[1],x[2],x[3],x[4][:150])
