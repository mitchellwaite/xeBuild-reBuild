"""python tools/wip/dehint/irfq.py <gen_irN.py> [-n TOP]: like irsweep, but also prints parseDump's frequencies from the optimized dump:
entry (bb 2) and the block holding the summary's last log, against connect_traces' threshold entry*100/1000 (the return block is copied when tail >= threshold)."""
import importlib.util, itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

a = sys.argv[1:]
top = 30
if '-n' in a:
    i = a.index('-n')
    top = int(a[i + 1])
    del a[i:i + 2]
s = importlib.util.spec_from_file_location('gen', a[0])
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
base = open(os.path.join(irlib.R, getattr(m, 'BASE', 'src/image_read.c')), newline='').read().replace('\r\n', '\n')
focus = getattr(m, 'FOCUS', None)


def one(c):
    t = base
    lab = '+'.join(x[0] for x in c if x[0])
    for l, ed in c:
        for x, y in ed:
            if x not in t:
                return lab, None, 'edit not found ' + x[:40], None
            t = t.replace(x, y)
    ok, o, d = irlib.compile_src(t, [], extra=['-fdump-tree-optimized-blocks-details'])
    if not ok:
        irlib.cleanup(d)
        return lab, None, o[:200], None
    idn, tot, per, notes = irlib.report(o)
    f = [x for x in os.listdir(d) if x.endswith('optimized')]
    txt = open(os.path.join(d, f[0]), errors='replace').read()
    irlib.cleanup(d)
    txt = txt[txt.find(';; Function parseDump'):]
    txt = txt[:txt.find(';; Function', 10)]
    fr = {}
    entry = tail = None
    cur = None
    for line in txt.split('\n'):
        mm = re.match(r';;\s+basic block (\d+), loop depth \d+, count \d+, freq (\d+)', line)
        if mm:
            cur = int(mm.group(2))
            if mm.group(1) == '2':
                entry = cur
        if '-----------------' in line:
            tail = cur
    k = sum(v for n, v in per.items() if n in focus) if focus else tot
    if idn:
        k = -1
    return lab, k, 'IDENTICAL' if idn else str(per), (entry, tail), t


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, list(itertools.product(*m.AXES))))
res.sort(key=lambda r: (r[1] if r[1] is not None else 1e9))
print(len(res), 'variants')
for r in res[:top]:
    print(r[1], '|', r[0] or '(base)', '| entry,tail', r[3], '|', r[2][:90])
name = os.path.splitext(os.path.basename(a[0]))[0]
if len(res[0]) > 4:
    open(os.path.join(irlib.BUILD, name + '_best.c'), 'w', newline='\n').write(res[0][4])
