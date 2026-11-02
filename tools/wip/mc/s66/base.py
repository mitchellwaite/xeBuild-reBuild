import sys,os,json
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
s=U.spec_from_file_location('q',os.path.join(D,'..','s64','q.py')); q=U.module_from_spec(s); s.loader.exec_module(q)
st=json.load(open(os.path.join(D,'..','s64','best_d.json'))); st['POST']=int(sys.argv[2])
mod=None
if len(sys.argv)>3: g={}; exec(open(sys.argv[3]).read(),g); mod=g['mod']
r,f,src=q.run(sys.argv[1],st,mod); print({k:r.get(k) for k in ('es2','per2','fncmp')} if r else r); print(f)
open(os.path.join(D,'o_%s.c'%sys.argv[1]),'w',newline='\n').write(src)
