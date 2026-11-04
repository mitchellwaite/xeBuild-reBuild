"""flxd.py <fl> <dead,dead,...> [edit,...]: unified diff of parseIni at a state (edits from flx3.EDITS)."""
import difflib, sys
import fllib as L, flx as X
try:
    import flx3
except ImportError:
    flx3 = None
fl = sys.argv[1]
dead = [d for d in sys.argv[2].split(',') if d]
if dead == ['all']:
    dead = X.ALLDEAD
ed = [e for e in sys.argv[3].split(',') if e] if len(sys.argv) > 3 else []
s = X.gen(dead, fl, ed)
o = L.compile(s, None, 'dd')
print(L.score(o)[:3])
for ln in difflib.unified_diff(L.dis(L.REF)['_parseIni'], L.dis(o)['_parseIni'], lineterm='', n=int(__import__('os').environ.get('CTX', 3))):
    print(ln)
