"""python tools/wip/dehint/iw_tuples.py <gen_iwN.py> [-n TOP] : run a generator (as iwsweep), and for each variant print the lines and
writeFsTable's iv compares (with names) from -fdump-tree-optimized.  Groups variants by whether each of the four (big copy) compares
has the reference's shape: `R` right order (end operand first in the big copy pair) etc.  Shows who moves what."""
import importlib.util, itertools, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def load(p):
    s = importlib.util.spec_from_file_location('gen', p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def one(c, text, flags):
    lab = '+'.join(x[0] for x in c if x[0]) or '(base)'
    for _, edits in c:
        for a, b in edits:
            if a not in text:
                return lab, None, 'edit not found'
            text = text.replace(a, b)
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='tu')
    try:
        ok, o, _ = iwlib.compile_src(text, flags, workdir=d, extra=['-fdump-tree-optimized'])
        if not ok:
            return lab, None, 'compile'
        idn, tot, per, notes = iwlib.report(o)
        f = [x for x in os.listdir(d) if x.endswith('optimized')]
        t = open(os.path.join(d, f[0]), errors='replace').read()
        b = re.search(r'^;; Function writeFsTable.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
        ifs = re.findall(r'if \(([\w.]*ivtmp[\w.]*|_\d+) != ([\w.]*ivtmp[\w.]*|_\d+)\)', b)
        tup = ' '.join(('i<e' if 'ivtmp' in x else 'e<i') + ':' + x.replace('ivtmp.', '') + ',' + y.replace('ivtmp.', '') for x, y in ifs)
        return lab, (0 if idn else tot), (per, tup)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    a = sys.argv[1:]
    top = 30
    if '-n' in a:
        i = a.index('-n')
        top = int(a[i + 1])
        del a[i:i + 2]
    m = load(a[0])
    text = open(os.path.join(iwlib.R, getattr(m, 'BASE', 'src/image_write.c')), newline='').read().replace('\r\n', '\n')
    flags = getattr(m, 'FLAGS', ['--param', 'builtin-expect-probability=50'])
    combos = list(itertools.product(*m.AXES))
    print(len(combos), 'variants', flush=True)
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda c: one(c, text, flags), combos))
    res = [r for r in res if r[1] is not None]
    res.sort(key=lambda r: r[1])
    seen = {}
    for lab, tot, (per, tup) in res:
        k = re.sub(r':[\w.,]+', '', tup)
        seen.setdefault(k, []).append((tot, lab, per, tup))
    for k, v in sorted(seen.items(), key=lambda kv: kv[1][0][0]):
        print(len(v), k)
        for tot, lab, per, tup in v[:3]:
            print('   ', tot, lab, per, tup[:150])
    if res and res[0][1] == 0:
        print('IDENTICAL', [r[0] for r in res if r[1] == 0][:20])


main()
