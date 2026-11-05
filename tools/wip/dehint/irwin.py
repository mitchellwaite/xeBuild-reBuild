"""python tools/wip/dehint/irwin.py <file.c> <old> <new> [lo hi step]: measurement only: replace old by new (with __builtin_expect in it) and compile with
builtin-expect-probability from lo to hi; prints getImageSmc's loose lines and irfeat-style flags for each.  The object's other expects move with it (exp_smc: pass `-` as `old` to probe it alone)."""
import os, re, sys
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

a = sys.argv[1:]
t = open(a[0], newline='').read().replace('\r\n', '\n')
if a[1] != '-':
    assert a[1] in t, 'old not found'
    t = t.replace(a[1], a[2])
lo, hi, st = (int(x) for x in (a[3:6] or (50, 96, 3)))
for n in range(lo, hi, st):
    ok, o, d = irlib.compile_src(t, ['--param', 'builtin-expect-probability=%d' % n])
    if not ok:
        print(o)
        break
    idn, tot, per, notes = irlib.report(o)
    fns, _ = irlib.disasm(o)
    irlib.cleanup(d)
    J = '\n'.join(re.sub(r'\s+', ' ', x.split(': ', 1)[1]) for x in fns['_getImageSmc'])
    f = 'A' if 'mov esi,ecx\nand esi,0xff00\nadd esi,eax' in J else '-'
    f += 'B' if 'lea eax,[ebx-0x800]\nmov edi,ebx' in J else '-'
    f += 'C' if 'mov edi,0x1000\nmov ebx,edi' in J else '-'
    zi, oi = J.find('mov DWORD PTR [esp+0x8],0x0\njmp'), J.find('mov ebx,edi\njmp')
    f += 'O' if 0 <= oi < zi else '-'
    print(n, per.get('_getImageSmc', 0), f, 'IDENTICAL' if idn else '')
