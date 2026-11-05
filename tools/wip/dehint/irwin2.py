"""python tools/wip/dehint/irwin2.py <file.c> <fn> <old> <new> [lo hi step]: measurement only, like irwin.py for any function: replace old by new (with __builtin_expect in it),
compile with builtin-expect-probability lo..hi, print fn's strict lines for each.  old `-` probes the file's expects as they are."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

a = sys.argv[1:]
t = open(a[0], newline='').read().replace('\r\n', '\n')
fn = a[1]
if a[2] != '-':
    assert a[2] in t, 'old not found'
    t = t.replace(a[2], a[3])
lo, hi, st = (int(x) for x in (a[4:7] or (40, 70, 1)))
for n in range(lo, hi, st):
    ok, o, d = irlib.compile_src(t, ['--param', 'builtin-expect-probability=%d' % n])
    if not ok:
        print(o)
        break
    idn, tot, per, notes = irlib.report(o)
    irlib.cleanup(d)
    print(n, per.get(fn, 0))
