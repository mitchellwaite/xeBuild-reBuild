import json,sys
rows=[json.loads(l) for l in open(sys.argv[1])]
rows=[r for r in rows if 'tinv' in r[2]]
rows.sort(key=lambda r:(r[2]['tinv'],r[2]['fncmp']))
for t,e,r in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 20]: print(r['tinv'],r['fncmp'],t,json.dumps(e)[:150],'|',r['o'][36:140])
