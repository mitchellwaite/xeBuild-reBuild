import json,sys
rows=[json.loads(l) for l in open(sys.argv[1])]
rows=[r for r in rows if r[2] is not None]
rows.sort(key=lambda r:(r[3][0],r[3][1]))
for t,d,sc,info in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 15]:
    print(info[0],info[1],t,json.dumps({k:v for k,v in d.items() if v}),'|',info[2][40:150])
