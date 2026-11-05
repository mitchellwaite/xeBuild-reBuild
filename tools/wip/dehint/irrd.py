"""python tools/wip/dehint/irrd.py <file.c>: where .rdata differs from the reference, by string (first few)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(t, [])
if not ok:
    print(o)
    sys.exit(1)
a = irlib.section(o, '.rdata')
b = irlib.ref()['sec']['.rdata']
sa = a.split(b'\0')
sb = b.split(b'\0')
n = 0
print(len(a), len(b))
for i, (x, y) in enumerate(zip(sa, sb)):
    if x != y:
        print(i, 'draft', x[:48], '| ref', y[:48])
        n += 1
        if n > 8:
            break
irlib.cleanup(d)
