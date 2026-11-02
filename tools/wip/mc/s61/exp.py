"""exp.py TAG MODFILE.py|- : text = s60 text(best169) passed through MOD(s) from MODFILE (def mod(s)); prints es2 + freqs."""
import sys,os,json,subprocess,io,contextlib
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(D,'..','s60')); sys.path.insert(0,os.path.join(D,'..','s53'))
import importlib.util as U
_sp=U.spec_from_file_location('sa60',os.path.join(D,'..','s60','sa.py')); S=U.module_from_spec(_sp); _sp.loader.exec_module(S)
import es2,es
R=es.R; BIN=os.path.join(R,'tools','toolchain-4745','mingw32','bin')
def base(): return S.text(json.load(open(os.path.join(D,'..','s60','best169.json'))))
def freqs(tag):
    sd=os.path.join(R,'build','v','mc42','slot_'+tag); out=os.path.join(sd,'det')
    os.makedirs(out,exist_ok=True)
    env=dict(os.environ,PATH=BIN+os.pathsep+os.environ['PATH'])
    subprocess.run([os.path.join(BIN,'gcc.exe'),'-S','-O3','-fno-toplevel-reorder','-fno-ipa-profile','-fno-reorder-functions','--param','builtin-expect-probability=50','-I'+os.path.join(R,'src'),'-fdump-rtl-compgotos-blocks-details',os.path.join(sd,'m.c'),'-o',os.path.join(out,'x.s')],cwd=out,env=env,capture_output=True)
    return subprocess.run([sys.executable,os.path.join(D,'fq.py'),sd,os.path.join(out,'m.c.267r.compgotos')],capture_output=True,text=True).stdout
if __name__=='__main__':
    tag=sys.argv[1]; s=base()
    if sys.argv[2]!='-':
        g={}; exec(open(sys.argv[2]).read(),g); s=g['mod'](s)
    r=es2.run(s,tag,True); print({k:r.get(k) for k in ('es2','per2','score','fncmp')} if r else r)
    print(freqs(tag))
