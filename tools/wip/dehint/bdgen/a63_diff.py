"""Attempt 63: unified diff of one function (loose form) between the reference build.o and a variant
from an a60lib-style script.  python tools/wip/dehint/bdgen/a63_diff.py <script.py> <label> [fn] [-p N]"""
import difflib, importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun
from a60lib import apply
a = sys.argv[1:]
p = 99
if '-p' in a:
    i = a.index('-p'); p = int(a[i + 1]); del a[i:i + 2]
spec = importlib.util.spec_from_file_location('v', a[0])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
fn = "_" + (a[2] if len(a) > 2 else "loadBlFiles")
t = apply(bdlib.read_src(), m.V[a[1]])
fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
ok, o, d = bdlib.compile_src(t, fl)
assert ok, o
fns, _ = bdlib.disasm(o)
r = bdlib.ref()['fns'][fn]
for l in difflib.unified_diff(bdrun.loose(r), bdrun.loose(fns[fn]), 'ref', 'var', n=3, lineterm=''):
    print(l)
bdlib.cleanup(d)
