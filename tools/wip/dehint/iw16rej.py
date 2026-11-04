"""python tools/wip/dehint/iw16rej.py <base.c> <out.log> [cap] [first] [last] [threads]: like iw14rejudge.py, but one compile per state that also writes writeFsTable's ivopts dump, so each
state has a compare signature (see iw15sig.py) as well as its lines. Log: `gen N: run of total, best lines, hist {sig: count}`; `SIG lines sig label genN per` for every state with the
target ivopts signature `<>><<` or the full optimized-dump signature `<>>><<<<` (the second includes split-paths' copies), source saved as build/iw/a16/sig_<gen>_<hash>.c; `BIG` lines count states with the big inner compare right whatever else is wrong (best per gen)."""
import collections, hashlib, importlib.util, itertools, os, random, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
TARGET = '<>><<'
TARGET8 = '<>>><<<<'
OUT = os.path.join(iwlib.BUILD, 'a16')
os.makedirs(OUT, exist_ok=True)
def sigscore(text):
    """(lines dict from iwlib, signature); same #line and stdin route as iwlib.compile_src"""
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='sr')
    dump = os.path.join(d, 'iv.txt')
    ok, o, d = iwlib.compile_src(text, [], workdir=d, extra=['-fdump-tree-ivopts=iv.txt', '-fdump-tree-optimized=op.txt'])
    try:
        if not ok:
            return {'compile': o[:300]}, ''
        idn, tot, per, notes = iwlib.report(o)
        tx = open(dump, errors='replace').read()
        m = re.search(r'^;; Function writeFsTable \(.*?(?=^;; Function |\Z)', tx, re.S | re.M)
        s = ''
        if m:
            b = m.group(0)
            b = b[b.find('\n{'):]
            for x in re.finditer(r'if \(ivtmp\.\d+_(\d+) != _(\d+)\)', b):
                s += '>' if int(x.group(1)) > int(x.group(2)) else '<'
        # full signature: the optimized dump's compares in order, split-paths' copies included
        tx = open(os.path.join(d, 'op.txt'), errors='replace').read()
        m = re.search(r'^;; Function writeFsTable \(.*?(?=^;; Function |\Z)', tx, re.S | re.M)
        s8 = ''
        if m:
            b = m.group(0)
            for x in re.finditer(r'if \((ivtmp\.\d+_\d+|_\d+) != (ivtmp\.\d+_\d+|_\d+)\)', b):
                if 'ivtmp' in x.group(0):
                    s8 += '<' if x.group(1).startswith('ivtmp') else '>'
        return {'identical': idn, 'total': tot, 'per': per, 'notes': notes, 'sig8': s8}, s
    finally:
        iwlib.cleanup(d)
if __name__ == '__main__':
    os.environ.setdefault('IWB', sys.argv[1])
    base = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
    log = open(sys.argv[2], 'a', newline='\n')
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    last = int(sys.argv[5]) if len(sys.argv) > 5 else 227
    th = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    here = os.path.dirname(os.path.abspath(__file__))
    seen = set()
    random.seed(16)
    ex = ThreadPoolExecutor(th)
    def run(a):
        n, lab, t = a
        r, s = sigscore(t)
        return n, lab, t, r, s
    for n in range(last, first - 1, -1):
        p = os.path.join(here, 'gen_iw%d.py' % n)
        if not os.path.exists(p):
            continue
        try:
            sp = importlib.util.spec_from_file_location('g', p)
            m = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(m)
            axes = m.AXES
        except BaseException as e:
            log.write('skip %d %s\n' % (n, str(e)[:80])); log.flush()
            continue
        keep = []
        for ax in axes:
            try:
                k = [o for o in ax if all(a in base for a, b in o[1])]
            except Exception:
                k = []
            if len(k) > 1:
                keep.append(k)
        if not keep:
            continue
        total = 1
        for k in keep:
            total *= len(k)
        combos = list(itertools.product(*keep)) if total <= cap else [tuple(random.choice(k) for k in keep) for _ in range(cap)]
        jobs = []
        for c in combos:
            t = base
            for lab, ed in c:
                for a, b in ed:
                    t = t.replace(a, b)
            h = hashlib.md5(t.encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            jobs.append((n, '+'.join(x[0] for x in c if x[0]), t))
        res = [r for r in ex.map(run, jobs) if 'compile' not in r[3]]
        res.sort(key=lambda r: r[3]['total'])
        hist = collections.Counter(r[3].get('sig8', '') for r in res)
        log.write('gen %d: %d of %d, best %s, hist %s\n' % (n, len(jobs), total, res[0][3]['total'] if res else '-', dict(hist)))
        for r in res:
            if r[4] == TARGET or r[3].get('sig8') == TARGET8 or r[3]['total'] == 0:
                h = hashlib.md5(r[2].encode()).hexdigest()[:8]
                open(os.path.join(OUT, 'sig_%d_%s.c' % (r[0], h)), 'w', newline='\n').write(r[2])
                log.write('SIG %d %s %s %s gen%d %s %s\n' % (r[3]['total'], r[4], r[3].get('sig8'), r[1][:80], r[0], h, iwlib.fmt(r[3])[:130]))
        log.flush()
    log.write('done\n'); log.close()
