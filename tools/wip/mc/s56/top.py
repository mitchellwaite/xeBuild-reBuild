import sys,json,glob,os
D=os.path.dirname(os.path.abspath(__file__)); L=[]
for f in glob.glob(os.path.join(D,'*.jsonl'))+glob.glob(os.path.join(D,'old','*.jsonl')):
    for l in open(f):
        try: L.append(json.loads(l))
        except Exception: pass
print('n',len(L))
z=[x for x in L if x['per2'].get('2',1)==0]; print('R2=0',len(z))
for x in sorted(z,key=lambda x:(x['es2'],x['per2'].get('3')))[:int(sys.argv[1]) if len(sys.argv)>1 else 5]: print(x['es2'],x['per2'],x['ev'],json.dumps(x['st'])[:300])
print('any'); [print(x['es2'],x['per2'],x['ev']) for x in sorted(L,key=lambda x:x['es2'])[:3]]
