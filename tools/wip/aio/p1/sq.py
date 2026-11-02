"""sq.py TAG [start]: role sequences (compressed) ref vs ours from first difference"""
import sys, lab, re
o=lab.orig_blocks(); m,ids=lab.our_blocks('../../../../build/v/aio_p1/%s/o.s'%sys.argv[1])
def c(l):
    r=[]
    for x in l:
        x=x.replace('-:.','.').replace('/jmp','^').replace('/jne','~').replace('/je','=').replace('strnicmp','S')
        r.append(x)
    return r
a,b=c(o),c(m)
k=0
while k<min(len(a),len(b)) and a[k]==b[k]: k+=1
print('common prefix',k,len(a),len(b))
print('R',' '.join(a[k:]))
print('M',' '.join(b[k:]))
