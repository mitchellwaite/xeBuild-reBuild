"""python tools/wip/dehint/irw16.py <file.c> <gen.py> <label> <P> [fn]: diff of one irwin3 point (attempt 16)."""
import difflib, importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
path, genp, lab, p = sys.argv[1:5]
fn = sys.argv[5] if len(sys.argv) > 5 else None
t = open(path, newline='').read().replace('\r\n', '\n')
s = importlib.util.spec_from_file_location('gen', genp)
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)
for a, b in g.REMOVE:
    t = t.replace(a, b)
old, new = g.TESTS[lab]
assert old in t
t = t.replace(old, new, 1)
if os.environ.get('IRAD'):
    import re
    ok, o, d = irlib.compile_src(t, ['--param', 'builtin-expect-probability=%s' % p], extra=['-fdump-rtl-ira-details'])
    q = [x for x in os.listdir(d) if '.ira' in x][0]
    x = open(os.path.join(d, q), errors='replace').read()
    x = x[x.index(';; Function %s ' % g.FN[1:]):]
    x = x[:x.index('\n;; Function ', 10)]
    for l in x.split('\n'):
        if re.search(r'Making|Pushing|Popping|^;; a\d+\(r\d+,l0\) conflicts', l):
            print(l)
ok, o, d = irlib.compile_src(t, ['--param', 'builtin-expect-probability=%s' % p])
assert ok, o
fns, _ = irlib.disasm(o)
irlib.cleanup(d)
fn = fn or g.FN
os.environ['IRLOOSE'] = '1'
for l in difflib.unified_diff(irlib.strip_addr(irlib.ref()['fns'][fn]), irlib.strip_addr(fns[fn]), lineterm='', n=1):
    print(l)
