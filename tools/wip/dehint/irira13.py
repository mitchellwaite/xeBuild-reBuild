"""python tools/wip/dehint/irira13.py <file.c> <fn> [regex]: IRA dump's coloring lines for fn (attempt 13): Pushing, Popping, Forming thread, Spilling."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
src, fn = sys.argv[1:3]
rx = re.compile(sys.argv[3] if len(sys.argv) > 3 else r'Popping|Assigning|Spilling|Forming thread|assign reg|Pushing|Disposition|^ *[0-9]+:r')
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-rtl-ira-details'])
if not ok:
    print(o); sys.exit(1)
fs = [x for x in os.listdir(d) if x.endswith('r.ira') or '.ira' in x]
t = open(os.path.join(d, fs[0]), errors='replace').read()
i = t.find(';; Function %s ' % fn)
t = t[i:]
j = t.find('\n;; Function ', 10)
t = t[:j] if j > 0 else t
for l in t.split('\n'):
    if rx.search(l):
        print(l)
irlib.cleanup(d)
