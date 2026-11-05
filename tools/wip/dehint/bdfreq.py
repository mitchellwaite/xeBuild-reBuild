"""python tools/wip/dehint/bdfreq.py <gen.py> <fn> regex[,regex..] [-n TOP] [-f fns]: like bdrun, with the block frequencies of fn's lines that match each regex
(summed per regex, from the .optimized dump) on every variant's line.  Sorted by loose lines."""
import glob, importlib.util, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun


def freqs(text, fn, pats):
    d = __import__('tempfile').mkdtemp(dir=bdlib.BUILD, prefix='f')
    src = '#line 1 "build.c"\n' + text
    subprocess.run([bdlib.GCC, '-c', '-O3'] + bdlib.P98 + ['-I' + os.path.join(bdlib.R, 'src'), '-fdump-tree-optimized-blocks-details', '-x', 'c', '-', '-o', 'o.o'],
                   input=src.encode(), cwd=d, capture_output=True)
    out = [[] for _ in pats]
    fs = glob.glob(os.path.join(d, '*.optimized'))
    if fs:
        p = False
        bb = 0
        for l in open(fs[0], errors='replace'):
            if l.startswith(';; Function '):
                p = l.split()[2] == fn
            elif p:
                m = re.match(r'\s*<bb \d+>|;;\s+basic block \d+, loop depth \d+, count \d+, freq (\d+)', l)
                if m and m.group(1):
                    bb = int(m.group(1))
                for i, q in enumerate(pats):
                    if q.search(l) and not l.lstrip().startswith(';;'):
                        out[i].append(bb)
    bdlib.cleanup(d)
    return out


def main():
    a = sys.argv[1:]
    top, focus = 40, None
    if '-n' in a:
        i = a.index('-n'); top = int(a[i + 1]); del a[i:i + 2]
    if '-f' in a:
        i = a.index('-f'); focus = a[i + 1].split(','); del a[i:i + 2]
    spec = importlib.util.spec_from_file_location('gen', a[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fn = a[1]
    pats = [re.compile(x) for x in a[2].split(',')]
    base = bdlib.read_src(os.path.join(bdlib.R, getattr(m, 'BASE', 'src/build.c')))
    if hasattr(m, 'PRE'):
        base = m.PRE(base)
    cases = m.CASES(base)

    def one(c):
        lab, f = c
        t = f(base) if callable(f) else f
        if t is None:
            return lab, {'err': 'skip'}, None
        return lab, bdrun.score(t), freqs(t, fn, pats)
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, cases))

    def key(x):
        r = x[1]
        if 'err' in r:
            return (10**9, 0)
        if focus:
            return (sum(v for k, v in r['L'].items() if k in focus), sum(v for k, v in r['S'].items() if k in focus))
        return (sum(r['L'].values()), sum(r['S'].values()))
    res.sort(key=key)
    for lab, r, q in res[:top]:
        if 'err' in r:
            print('ERR', lab, r['err'][:200])
        else:
            print('%s L%d S%d | %s | %s | %s %s' % ('IDENTICAL' if r['identical'] else '', sum(r['L'].values()), sum(r['S'].values()), lab, ' '.join('+'.join(map(str, x)) for x in q),
                                                   ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])))


main()
