"""python tools/wip/dehint/irwin3.py <file.c> <gen.py>: measurement only, windows of many tests.
gen defines FN (function), REMOVE [(old, new)...] applied first, TESTS {label: (old, cond)}: `old` is replaced
with `new` where the test's condition cond appears wrapped in __builtin_expect(!!(cond), 1); P = 5..95 by 5 (or gen.PS).
Prints for each test the FN lines (strict/loose are the same run: strict) at each P, and any IDENTICAL.
"""
import importlib.util, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib


def main():
    t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
    s = importlib.util.spec_from_file_location('gen', sys.argv[2])
    g = importlib.util.module_from_spec(s)
    s.loader.exec_module(g)
    for a, b in g.REMOVE:
        assert a in t, a
        t = t.replace(a, b)
    ps = getattr(g, 'PS', list(range(5, 100, 5)))

    def one(job):
        lab, text, p = job
        ok, o, d = irlib.compile_src(text, ['--param', 'builtin-expect-probability=%d' % p])
        if not ok:
            return lab, p, o[:200]
        idn, tot, per, notes = irlib.report(o)
        irlib.cleanup(d)
        return lab, p, 'ID' if idn else per.get(g.FN, 0) if tot == per.get(g.FN, 0) else '%s/%d' % (per.get(g.FN, 0), tot)

    jobs = []
    ok, o, d = irlib.compile_src(t, [])
    idn, tot, per, notes = irlib.report(o)
    irlib.cleanup(d)
    print('base', 'ID' if idn else per)
    for lab, (old, new) in g.TESTS.items():
        assert old in t, old
        tt = t.replace(old, new, 1)
        for p in ps:
            jobs.append((lab, tt, p))
    res = {}
    with ThreadPoolExecutor(os.cpu_count()) as ex:
        for lab, p, r in ex.map(one, jobs):
            res.setdefault(lab, []).append('%d:%s' % (p, r))
    for lab in res:
        print(lab, ' '.join(res[lab]), flush=True)


main()
