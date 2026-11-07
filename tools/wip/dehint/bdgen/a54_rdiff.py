"""Attempt 54: diff one function of a variant against the reference (- reference, + variant), p99.
python tools/wip/dehint/bdgen/a54_rdiff.py <variant.c> <_symbol> [p]"""
import difflib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdlib
p = int(sys.argv[3]) if len(sys.argv) > 3 else 99
fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
ok, o, d = bdlib.compile_src(open(sys.argv[1], newline='').read(), fl)
if not ok:
    sys.exit(o)
x = bdlib.disasm(bdlib.REF)[0].get(sys.argv[2], [])
y = bdlib.disasm(o)[0].get(sys.argv[2], [])
for l in difflib.unified_diff(x, y, lineterm='', n=3):
    print(l)
