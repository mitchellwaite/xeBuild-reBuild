"""sq2.py TAG: print only differing runs (ref vs ours) using SequenceMatcher on role seq"""
import sys, lab, re, difflib
o=lab.orig_blocks(); m,ids=lab.our_blocks('../../../../build/v/aio_p1/%s/o.s'%sys.argv[1])
def c(l):
    return [x.replace('-:.','.').replace('/jmp','^').replace('/jne','~').replace('/je','=').replace('strnicmp','S') for x in l]
a,b=c(o),c(m)
print(len(a),len(b))
for t,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if t!='equal':
        print(i1,j1,'R:',' '.join(a[i1:i2])[:600]); print('    M:',' '.join(b[j1:j2])[:600])
