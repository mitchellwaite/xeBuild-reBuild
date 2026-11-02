"""hc.py: greedy hill-climb on rok weights + cap, objective es2 (ties: R3). log hc.jsonl"""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(D,'..','s54')); sys.path.insert(0,os.path.join(D,'..','s53'))
import rkgen,lev,es2
def ev(w,cap,tag):
    old=rkgen.mk; rkgen.mk=lambda ww,base=None: old(ww,cap=cap,base=base)
    try: txt=lev.text({'w':w})
    finally: rkgen.mk=old
    r=es2.run(txt,tag,False); return (r['es2'] if r else 9999),(r and r['per2']),txt
w=json.loads(sys.argv[1]); cap=int(sys.argv[2]); rounds=int(sys.argv[3])
best,per,txt=ev(w,cap,'s55h'); print('start',best,per,flush=True)
L=rkgen.RL+['_ft']
for rd in range(rounds):
    imp=False
    for l in L:
        for d in (1,-1):
            n=dict(w); n[l]=n.get(l,0)+d
            if n[l]<0: continue
            s,p,t=ev(n,cap,'s55h')
            with open(os.path.join(D,'hc.jsonl'),'a') as f: f.write(json.dumps({'w':n,'cap':cap,'es2':s,'per':p})+'\n')
            if s<best: best,per,w,txt,imp=s,p,n,t,True; print('imp',best,per,w,flush=True); open(os.path.join(D,'hc_best.c'),'w',newline='\n').write(txt)
    if not imp: break
print('final',best,per,w)
