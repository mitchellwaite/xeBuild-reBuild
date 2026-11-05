"""python tools/wip/dehint/irwin2.py <file.c> <fn> <lo> <hi> <step> [old new]: measurement only: <fn>'s loose lines at each builtin-expect-probability, with an optional source edit."""
import os, sys
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

a = sys.argv[1:]
t = open(a[0], newline='').read().replace('\r\n', '\n')
if len(a) > 5:
    assert a[5] in t
    t = t.replace(a[5], a[6])
for n in range(int(a[2]), int(a[3]), int(a[4])):
    ok, o, d = irlib.compile_src(t, ['--param', 'builtin-expect-probability=%d' % n])
    if not ok:
        print(o)
        break
    idn, tot, per, notes = irlib.report(o)
    irlib.cleanup(d)
    print(n, per.get(a[1], 0), tot, 'IDENTICAL' if idn else '')
