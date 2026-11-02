import sys,os,json,copy
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
s=U.spec_from_file_location('cp',os.path.join(D,'cp.py')); cp=U.module_from_spec(s); s.loader.exec_module(cp)
base=json.load(open(os.path.join(D,'..','s64','best_d.json')))
def ev(name,f):
    st=copy.deepcopy(base); f(st); src=cp.text(st,[])
    import re; m=re.search(r'AT\(c3\)[^\n]*',src)
    r=cp.SA.T.es2.run(src,name,True)
    print(name,{k:r.get(k) for k in ('es2','per2','fncmp')} if r else r,m.group(0)[:90] if m else None,flush=True)
    json.dump(st,open(os.path.join(D,'x3_%s.json'%name),'w'))
V={'x0':lambda s:s['X'].pop('c3'),'x1':lambda s:s['X'].__setitem__('c3',1),'x3':lambda s:s['X'].__setitem__('c3',3),
 'w0':lambda s:s['w'].__setitem__('c3',0),'w2':lambda s:s['w'].__setitem__('c3',2),'th0':lambda s:s.__setitem__('TH',[t for t in s['TH'] if t[0]!='c3']),
 'x0th0':lambda s:(s['X'].pop('c3'),s.__setitem__('TH',[t for t in s['TH'] if t[0]!='c3']))}
for n in (sys.argv[1:] or V): ev(n,V[n])
