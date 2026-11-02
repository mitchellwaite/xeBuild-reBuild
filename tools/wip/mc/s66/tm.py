import sys,os,json,subprocess
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
s=U.spec_from_file_location('cp',os.path.join(D,'cp.py')); cp=U.module_from_spec(s); s.loader.exec_module(cp)
base=json.load(open(os.path.join(D,'..','s64','best_d.json')))
src=cp.text(base,[])
for a,b in zip(sys.argv[2::2],sys.argv[3::2]):
    assert src.count(a)==1,a; src=src.replace(a,b)
r=cp.SA.T.es2.run(src,sys.argv[1],True)
o=subprocess.run(['python',os.path.join(D,'..','s61','rk.py'),sys.argv[1],'3'],capture_output=True,text=True).stdout
print(sys.argv[1],{k:r.get(k) for k in ('es2','per2','fncmp')} if r else r,flush=True); print(o)
open(os.path.join(D,'o_%s.c'%sys.argv[1]),'w',newline='\n').write(src)
