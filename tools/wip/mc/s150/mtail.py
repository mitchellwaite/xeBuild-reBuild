# mtail.py DUMP "[changes python list]" : model tail for real2-style changes
import sys,ast
sys.argv_=sys.argv
import importlib.util as u
sp=u.spec_from_file_location('real2',r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s150\real2.py'); m=u.module_from_spec(sp); sp.loader.exec_module(m)
m.init(sys.argv[1]); cs=ast.literal_eval(sys.argv[2])
gg=dict(m.g)
for n,c in sorted(enumerate(cs),key=lambda x:(-x[1][2],x[0])):
    L=list(gg[c[1]]); L.insert(c[2],('ins','this',m.D+1+n,c[3]) if c[0]=='dum' else ('ins','this',c[3],m.KEY[c[3]])); gg[c[1]]=L
o=m.r4sim.sim(m.pre,gg,{}); print(o[12:36]); print(m.TGT[12:36])
