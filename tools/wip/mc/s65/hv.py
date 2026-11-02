import sys,os,json,copy,time
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
s=U.spec_from_file_location('q',os.path.join(D,'..','s64','q.py')); q=U.module_from_spec(s); s.loader.exec_module(q)
base=json.load(open(os.path.join(D,'..','s64','best_d.json')))
def V(name,f):
    st=copy.deepcopy(base); f(st)
    try: r,_,src=q.run('h65'+name,st)
    except Exception as e: print(name,'ERR',e); return
    print(name,{k:r.get(k) for k in ('es2','per2','fncmp')} if r else r,flush=True)
    json.dump(st,open(os.path.join(D,'v_%s.json'%name),'w'))
def pdset(c,d):
    def f(st):
        st['PD']=[p for p in st['PD'] if p[0]!='c11']+([[c,d]] if d else [])
    return f
def wset(k,v):
    def f(st): st['w'][k]=v
    return f
def thdrop(k):
    def f(st): st['TH']=[t for t in st['TH'] if t[0]!=k]
    return f
VS={'base':lambda st:None,'pd0':pdset('c11',0),'pd8':pdset('c11',8),'pd9':pdset('c11',9),
 'w2':wset('c11',2),'w1':wset('c11',1),'w4':wset('c11',4),'th0':thdrop('c11'),
 'pd0w4':lambda st:(pdset('c11',0)(st),wset('c11',4)(st)),'x0':lambda st:st['X'].pop('c11',None),
 'o0':lambda st:st['order'].remove('c11'),'w0':wset('c11',0),'o0w0':lambda st:(st['order'].remove('c11'),wset('c11',0)(st)),
 'w0x2':lambda st:(wset('c11',0)(st),st['X'].__setitem__('c11',2)),'o0w2':lambda st:(st['order'].remove('c11'),wset('c11',2)(st))}
for n in (sys.argv[1:] or VS): V(n,VS[n])
