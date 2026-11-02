"""q.py TAG STATE.json [MOD.py]: s62 text(state) [-> mod(s)], es2 + fq table."""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
def L(n,p):
    s=U.spec_from_file_location(n,p); m=U.module_from_spec(s); s.loader.exec_module(m); return m
T=L('sa62',os.path.join(D,'..','s62','sa.py')); X=L('exp61',os.path.join(D,'..','s61','exp.py'))
def run(tag,st,mod=None):
    th=st.get('TH',[]); st=T.S.fix(st); st['TH']=th; s=T.text(st)
    if mod: s=mod(s)
    r=T.es2.run(s,tag,True); return r,X.freqs(tag),s
if __name__=='__main__':
    st=json.load(open(sys.argv[2])); mod=None
    if len(sys.argv)>3: g={}; exec(open(sys.argv[3]).read(),g); mod=g['mod']
    r,f,s=run(sys.argv[1],st,mod); print({k:r.get(k) for k in ('es2','per2','score','fncmp')} if r else r); print(f)
    open(os.path.join(D,'last_%s.c'%sys.argv[1]),'w',newline='\n').write(s)
