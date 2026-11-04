"""fl5s.py <helpers> [tests] [nlines]: show the parseIni diff (branch targets blanked) for one state.
helpers like 'flash:t,sec' or '-'; tests like 'raw,off3'."""
import difflib, sys
import fllib as L, fl5lib as F

sp = sys.argv[1]
h = {} if sp == '-' else dict(x.split(':') if ':' in x else (x, '') for x in sp.split(','))
t = tuple(sys.argv[2].split(',')) if len(sys.argv) > 2 and sys.argv[2] != '-' else ()
o = L.compile(F.gen(t, True, h), None, 'a5show')
print(L.score(o)[:3], F.nscore(o))
a, b = F.norm(L.dis(L.REF))['_parseIni'], F.norm(L.dis(o))['_parseIni']
n = int(sys.argv[3]) if len(sys.argv) > 3 else 80
ls = list(difflib.unified_diff(a, b, lineterm='', n=1))
print('\n'.join(ls[:n]))
