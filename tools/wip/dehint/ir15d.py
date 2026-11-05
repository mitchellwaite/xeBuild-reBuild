"""python tools/wip/dehint/ir15d.py <file.c> <fn> : loose unified diff of one function against the reference (calls and relocs dropped), then
the object's .rdata strings where they first differ, and the block chain of the optimized dump with each log's string."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['IRLOOSE'] = '1'
import irlib
text = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
fn = sys.argv[2]
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-tree-optimized'])
if not ok:
    print(o)
    sys.exit(1)
fns, _ = irlib.disasm(o)
a = [l for l in irlib.strip_addr(irlib.ref()['fns'][fn]) if not re.match(r'(call|DISP32|dir32)', l)]
b = [l for l in irlib.strip_addr(fns[fn]) if not re.match(r'(call|DISP32|dir32)', l)]
print('\n'.join(difflib.unified_diff(a, b, 'ref', 'draft', lineterm='', n=1)))
rd = irlib.section(o, '.rdata')
rr = irlib.ref()['sec']['.rdata']
if rd != rr:
    i = next((k for k, (x, y) in enumerate(zip(rd, rr)) if x != y), None)
    print('.rdata differs at', i, 'ref', rr[i:i + 50] if i is not None else '', 'got', rd[i:i + 50] if i is not None else '')
fname = fn.lstrip('_')
f = [x for x in os.listdir(d) if x.endswith('optimized')][0]
t = open(os.path.join(d, f), errors='replace').read()
t = t[t.find(';; Function %s ' % fname):]
j = t.find('\n;; Function ', 10)
t = t[:j] if j > 0 else t
for l in t.split('\n'):
    if re.match(r'\s*<bb \d+>', l):
        print(l.strip(), end=' ')
    m = re.search(r'log_printf \(1, "(.{0,60})', l)
    if m:
        print('[' + m.group(1)[:44] + ']', end=' ')
    if 'goto <bb' in l or 'return' in l:
        print(l.strip()[:18], end=' ')
    if re.search(r'^\s*if ', l):
        print('\n   ' + l.strip(), end=' ')
    if not l.strip():
        print()
irlib.cleanup(d)
