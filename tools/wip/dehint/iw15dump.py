import os,subprocess,sys,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import iwlib
# python tools/wip/dehint/iw15dump.py <name> <file.c> [flags]: all tree dumps with .MEM names (-vops) plus pre-details, into build/iw/a15/d_<name>; input for iw15stack.py, iw15src.py, iw14pop.py, iw15pre.py
name,path=sys.argv[1],sys.argv[2]
d=os.path.join(iwlib.BUILD,'a15','d_'+name); os.makedirs(d,exist_ok=True)
open(os.path.join(d,'a.c'),'w',newline='\n').write(open(path,newline='').read().replace('\r\n','\n'))
for f in glob.glob(d+'/a.c.*'): os.remove(f)
r=subprocess.run([iwlib.GCC,'-c','-O3','-I'+os.path.join(iwlib.R,'src'),'-fdump-tree-all-vops','-fdump-tree-pre-details-vops','a.c','-o','a.o']+sys.argv[3:],cwd=d,stdin=subprocess.DEVNULL)
print(r.returncode,d)
