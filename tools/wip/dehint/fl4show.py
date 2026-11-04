"""fl4show.py <dead label> <secs +list>: diff of parseIni."""
import difflib, sys
import fllib as L, fl4lib as F
o = L.compile(F.gen(F.st(sys.argv[1]), sys.argv[2].split('+') if sys.argv[2] else ()), None, 'a4show')
print(L.score(o)[:3], F.vec(o))
for k, v in L.dis(L.REF).items():
    w = L.dis(o).get(k, [])
    if v != w:
        for ln in difflib.unified_diff(v, w, lineterm='', n=3):
            print(ln)
