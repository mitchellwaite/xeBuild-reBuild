import json,sys
L=[json.loads(l) for l in open(sys.argv[1])]
L=[x for x in L if 'score' in x]; print(len(L), 'errs')
for x in sorted(L,key=lambda x:(x['score'],x['fncmp']))[:int(sys.argv[2]) if len(sys.argv)>2 else 12]: print(x['score'],x['fncmp'],x['nev'],x['e'],x['df'],x['o'][:90])
print('67:', [(x['e'],x['df'],x['score']) for x in L if '67' in x['df']][:10])
