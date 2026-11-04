"""python tools/wip/dehint/iw25fr.py <gen.py> [threads] (base from IWB): each state of a generator: lines per function, plus imgAdd's depth-1 tests with their frequencies at fnsplit (just after profile_estimate), and the same in the optimized dump."""
import importlib.util, itertools, os, re, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
gen = sys.argv[1]; th = int(sys.argv[2]) if len(sys.argv) > 2 else 4
sp = importlib.util.spec_from_file_location('g', gen); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
base = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a24.c')
text = open(os.path.join(iwlib.R, base), newline='').read().replace('\r\n', '\n')


def tests(fn_text, name='imgAdd', n=5):
    m = re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)' % (name, name), fn_text, re.S | re.M)
    if not m:
        return []
    b = m.group(0)
    b = b[b.find('\n%s (' % name):]
    out = []
    for x in re.split(r'(?=;;   basic block)', b):
        h = re.search(r'basic block (\d+), loop depth (\d), count \d+, freq (\d+)', x)
        c = re.findall(r'if \(([^\n]*)\)', x)
        if h and c and h.group(2) == '1':
            out.append('%s:%s' % (h.group(3), re.sub(r'_\d+|\(D\)', '', c[0])[:18]))
    return out[:n]


def one(c):
    lab = '+'.join(x[0] for x in c if x[0])
    t = text
    for l, ed in c:
        for x, y in ed:
            if x not in t:
                return lab, 'missing ' + x[:60], '', ''
            t = t.replace(x, y)
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='fr')
    ok, o, d = iwlib.compile_src(t, [], workdir=d, extra=['-fdump-tree-fnsplit-blocks-details=fs.txt', '-fdump-tree-optimized-blocks-details=op.txt'])
    try:
        if not ok:
            return lab, 'compile ' + o[:200], '', ''
        idn, tot, per, notes = iwlib.report(o)
        q = {a.replace('_imgAdd', '').replace('.constprop', '') or 'A': b for a, b in per.items()}
        return lab, ('IDENTICAL' if idn else '%d %s' % (tot, q)), tests(open(os.path.join(d, 'fs.txt'), errors='replace').read()), tests(open(os.path.join(d, 'op.txt'), errors='replace').read(), n=3)
    finally:
        iwlib.cleanup(d)


res = list(ThreadPoolExecutor(th).map(one, list(itertools.product(*m.AXES))))
res.sort(key=lambda r: int(r[1].split()[0]) if r[1][0].isdigit() else (0 if r[1] == 'IDENTICAL' else 10**9))
for r in res:
    print(r[0], r[1][:120], '\n    ', r[2], r[3])
