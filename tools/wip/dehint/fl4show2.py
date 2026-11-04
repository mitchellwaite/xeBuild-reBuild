"""fl4show2.py <module> <V key parts>: show the diff of a generator's state: python fl4show2.py c 'W|0|label'"""
import difflib, sys
import fllib as L, fl4lib as F
import fl4c as C
m, c, x = sys.argv[1].split('|')
o = L.compile(C.gen(m, int(c), x.split('+') if x else ()), None, 'a4show')
print(L.score(o)[:3], F.vec(o))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 60
for k, v in L.dis(L.REF).items():
    w = L.dis(o).get(k, [])
    if v != w:
        print('=== ', k, len(v), len(w))
        for ln in list(difflib.unified_diff(v, w, lineterm='', n=1))[:n]:
            print(ln)
