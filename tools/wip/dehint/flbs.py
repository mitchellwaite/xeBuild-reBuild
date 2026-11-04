"""flbs.py <tag> <fn>: diff of an already compiled variant object against the reference."""
import difflib,sys
import fllib as L
o=L.OUT+'/'+sys.argv[1]+'.o'
for ln in difflib.unified_diff(L.dis(L.REF)['_'+sys.argv[2]],L.dis(o)['_'+sys.argv[2]],lineterm='',n=int(sys.argv[3]) if len(sys.argv)>3 else 2): print(ln)
