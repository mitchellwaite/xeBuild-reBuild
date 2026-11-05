"""python tools/wip/dehint/irprof13.py <file.c> <fn> : the profile_estimate dump's predictions and blocks (attempt 13)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
src, fn = sys.argv[1:3]
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-tree-profile_estimate-blocks-details'])
if not ok:
    print(o); sys.exit(1)
f = [x for x in os.listdir(d) if 'profile_estimate' in x][0]
t = open(os.path.join(d, f), errors='replace').read()
i = t.find(';; Function %s ' % fn)
t = t[i:]
j = t.find('\n;; Function ', 10)
t = t[:j] if j > 0 else t
for l in t.split('\n'):
    if re.search(r'heuristics|^Predictions for bb|^\s+# (SUCC|PRED|BLOCK)|^<bb|if \(|return|log_printf|calloc', l) :
        print(l[:110])
irlib.cleanup(d)
