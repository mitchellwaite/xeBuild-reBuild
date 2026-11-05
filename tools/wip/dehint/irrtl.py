"""python tools/wip/dehint/irrtl.py <file.c> <fn> <pass> [pass ...]: slim RTL dump of fn after the named passes (expand, cse1, ce1, ira, reload, jump2, ce3, bbro, ...)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
src, fn = sys.argv[1:3]
passes = sys.argv[3:]
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-rtl-%s-slim-blocks' % p for p in passes])
if not ok:
    print(o)
    sys.exit(1)
for p in passes:
    fs = [x for x in os.listdir(d) if x.endswith('.' + p) or re.search(r'r\.%s$' % p, x)]
    if not fs:
        print('no', p, os.listdir(d)[:8])
        continue
    t = open(os.path.join(d, fs[0]), errors='replace').read()
    i = t.find(';; Function %s ' % fn)
    t = t[i:]
    j = t.find('\n;; Function ', 10)
    if j > 0:
        t = t[:j]
    print('=====', p)
    print(t)
irlib.cleanup(d)
