"""Attempt 25, mechanism probe (not a candidate): how far can imgAdd be rescaled before each clone breaks?
A table of k entries in a real arm with __builtin_expect on its test and builtin-expect-probability=N makes the table's
loop head about f * N% * k, so the rescale can be stepped finely. All these arms are in the `type > 1` body, dead in every
clone (their types are 0 and 1), so what reaches a clone is only the rescale; imgAdd itself also sees the expect's names.
python tools/wip/dehint/iw25probe.py [base.c] [threads] [lo] [hi]: for states with the page loop's head in lo..hi, prints
arm, k, N, head and lines per function."""
import os, re, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(iwlib.R, 'tools/wip/dehint/drafts/image_write_a24.c')
th = int(sys.argv[2]) if len(sys.argv) > 2 else 4
text = open(base, newline='').read().replace('\r\n', '\n')
T5, T6, T7 = '\t' * 5, '\t' * 6, '\t' * 7


def tab(k, ind, stmt):
    return ('%sint part[%d] = { 4 };\n%sint sum = 0, j;\n\n%sfor (j = 0; j < %d; j++)\n%s\tsum += part[j];\n%s%s\n') % (ind, k, ind, ind, k, ind, ind, stmt)


ARMS = {
    'p3': (T6 + 'if (pages & 3)\n' + T7 + 'pages = (pages + 4) & ~3;\n',
           T6 + 'if (__builtin_expect((pages & 3) != 0, 1)) {\n%s' + T6 + '}\n', T7, 'pages = (pages + sum) & ~3;'),
    's5': (T6 + 'if (type == 0x2c)\n' + T7 + 's[5] = 1;\n',
           T6 + 'if (__builtin_expect(type == 0x2c, 1)) {\n%s' + T6 + '}\n', T7, 's[5] = sum - 3;'),
    's8': (T5 + "if (type != '0') {\n" + T6 + 's[8] = len >> 8;\n' + T6 + 's[7] = len;\n' + T5 + '}\n',
           T5 + "if (__builtin_expect(type != '0', 1)) {\n%s" + T5 + '}\n', T6, 's[8] = (len >> 8) + sum - 4;\n' + T6 + 's[7] = len;'),
}


def build(arm, k):
    o, w, ind, st = ARMS[arm]
    assert o in text, arm
    return text.replace(o, w % tab(k, ind, st))


def pagehead(fs, fn='imgAdd'):
    m = re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)' % (fn, fn), fs, re.S | re.M).group(0)
    m = m[m.find('\n%s (' % fn):]
    pm = re.search(r'freq (\d+)[^\n]*\n(?:[^\n]*\n){0,14}?\s*if \(p_\d+ < end_\d+\)', m)
    return int(pm.group(1)) if pm else None


def one(a):
    arm, k, n = a
    t = build(arm, k)
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='pr')
    ok, o, d = iwlib.compile_src(t, ['--param', 'builtin-expect-probability=%d' % n], workdir=d, extra=['-fdump-tree-fnsplit-blocks-details=fs.txt'])
    try:
        if not ok:
            return arm, k, n, None, o[:200]
        h = pagehead(open(os.path.join(d, 'fs.txt'), errors='replace').read())
        idn, tot, per, notes = iwlib.report(o)
        return arm, k, n, h, per
    finally:
        iwlib.cleanup(d)


if __name__ == '__main__':
    lo, hi = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (9900, 10000)
    jobs = [(arm, k, n) for arm in ARMS for k in range(3, 17) for n in range(20, 100)]
    res = list(ThreadPoolExecutor(th).map(one, jobs))
    res = [r for r in res if r[3] and lo <= r[3] <= hi]
    res.sort(key=lambda r: r[3], reverse=True)
    for arm, k, n, head, per in res:
        q = {a.replace('_imgAdd', '').replace('.constprop', '') or 'A': b for a, b in per.items()}
        print(arm, 'k', k, 'N', n, 'head', head, q, flush=True)
