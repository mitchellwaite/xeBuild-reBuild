import sys,os,json,copy,subprocess
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
s=U.spec_from_file_location('cp',os.path.join(D,'cp.py')); cp=U.module_from_spec(s); s.loader.exec_module(cp)
base=json.load(open(os.path.join(D,'..','s64','best_d.json')))
def ev(name,st):
    r=cp.SA.T.es2.run(cp.text(st,[]),name,True)
    o=subprocess.run(['python',os.path.join(D,'..','s61','rk.py'),name,'3'],capture_output=True,text=True).stdout
    print(name,{k:r.get(k) for k in ('es2','per2','fncmp')} if r else r,'1114' in o,'109,' in o,flush=True)
    json.dump(st,open(os.path.join(D,'th_%s.json'%name),'w'))
for i in range(len(base['TH'])):
    st=copy.deepcopy(base); st['TH'].pop(i); ev('t%d'%i,st)
for i in range(len(base['PD'])):
    st=copy.deepcopy(base); st['PD'].pop(i); ev('p%d'%i,st)
