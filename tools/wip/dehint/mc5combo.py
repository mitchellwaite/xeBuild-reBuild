"""mode_client attempt 5: score one combination of mc1 edit keys on MCBASE (default src).

python tools/wip/dehint/mc5combo.py KEY [KEY ...] [-v] [-o OUT.c]"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

a = sys.argv[1:]
keys = [k for k in a if not k.startswith('-') and not k.endswith('.c')]
t = mc1.build_template(mc1lib.read_src(mc1.BASE))
es = {e[0]: e for e in mc1.edits(t)}
m = ({}, {}, [])
for k in keys:
    m = mc1.merge(m, es[k][1:])
    if m is None:
        sys.exit('conflict at ' + k)
text = mc1.render(t, *m)
if '-o' in a:
    open(a[a.index('-o') + 1], 'w', newline='\n').write(text)
if '-v' in a:
    mc1lib.vdiff(text)
else:
    print(mc1lib.fmt(mc1lib.score_text(text)), mc1.count(text)['total'])
