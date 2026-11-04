"""Attempt 25, mechanism probe (not a candidate): finer steps of the rescale than iw25probe.py, with two expects in a row so the table's
loop head is about 1661 * (N/100)^2 * (k+1). Same reading: every arm here is dead in the clones, so a clone's lines come from the rescale.
python tools/wip/dehint/iw25probe2.py [lo] [hi] [base.c] : all (k, N) with a predicted head above 10000 in lo..hi."""
import os, re, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

lo = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 10110
base = sys.argv[3] if len(sys.argv) > 3 else os.path.join(iwlib.R, 'tools/wip/dehint/drafts/image_write_a24.c')
text = open(base, newline='').read().replace('\r\n', '\n')
T6, T7, T8 = '\t' * 6, '\t' * 7, '\t' * 8
OLD = T6 + 'if (pages & 3)\n' + T7 + 'pages = (pages + 4) & ~3;\n'
assert OLD in text


def build(k):
    return text.replace(OLD, T6 + 'if (__builtin_expect((pages & 3) != 0, 1)) {\n'
                        + T7 + 'if (__builtin_expect((pages & 1) != 0, 1)) {\n'
                        + T8 + 'int part[%d] = { 4 };\n' % k + T8 + 'int sum = 0, j;\n\n'
                        + T8 + 'for (j = 0; j < %d; j++)\n' % k + T8 + '\tsum += part[j];\n'
                        + T8 + 'pages = (pages + sum) & ~3;\n'
                        + T7 + '} else\n' + T8 + 'pages = (pages + 4) & ~3;\n' + T6 + '}\n')


def pagehead(fs, fn='imgAdd'):
    m = re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)' % (fn, fn), fs, re.S | re.M).group(0)
    m = m[m.find('\n%s (' % fn):]
    pm = re.search(r'freq (\d+)[^\n]*\n(?:[^\n]*\n){0,14}?\s*if \(p_\d+ < end_\d+\)', m)
    return int(pm.group(1)) if pm else None


def one(a):
    k, n = a
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='pr')
    ok, o, d = iwlib.compile_src(build(k), ['--param', 'builtin-expect-probability=%d' % n], workdir=d, extra=['-fdump-tree-fnsplit-blocks-details=fs.txt'])
    try:
        if not ok:
            return k, n, None, o[:200]
        h = pagehead(open(os.path.join(d, 'fs.txt'), errors='replace').read())
        return (k, n, h) + iwlib.report(o)[2:3]
    finally:
        iwlib.cleanup(d)


if __name__ == '__main__':
    jobs = [(k, n) for k in range(2, 17) for n in range(40, 100) if lo <= 1661 * (n / 100) ** 2 * (k + 1) <= hi]
    print(len(jobs), 'jobs', flush=True)
    res = sorted(ThreadPoolExecutor(4).map(one, jobs), key=lambda r: -(r[2] or 0))
    for k, n, h, per in res:
        q = {a.replace('_imgAdd', '').replace('.constprop', '') or 'A': b for a, b in per.items()}
        print('k', k, 'N', n, 'head', h, 'clones', {x: q[x] for x in q if x[0] == '.'}, 'A', q.get('A', 0), 'File', q.get('File', 0), flush=True)
