"""flxm.py <label> [save path]: diff (or save) an arm-size state from flxk (`nest|a=1,b=2|t`)."""
import difflib, sys
import fllib as L, flxk as K


def parse(lb):
    a = lb.split('|')
    keep = dict((kv.split('=')[0], int(kv.split('=')[1])) for kv in a[1].split(',') if kv)
    return a[0], keep, len(a) > 2


s = K.build(*parse(sys.argv[1]))
if len(sys.argv) > 2:
    open(sys.argv[2], 'w', newline='\n').write(s)
o = L.compile(s, None, 'xm')
print(L.score(o)[:4])
for ln in difflib.unified_diff(L.dis(L.REF)['_parseIni'], L.dis(o)['_parseIni'], lineterm='', n=1):
    print(ln)
