"""The hints left in src/build.c as named edits, for generators, and their cost alone when run directly.

python tools/wip/dehint/bdhints.py [name,name ...]: with no arguments every hint's strict/loose lines removed alone; with arguments, score each set.
Generators: `import bdhints; bdhints.off(text, 'pin_size', ...)`; `off` raises if a hint's text isn't there."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun

H = {
    'exp_t10': [('__builtin_expect(type == 10, 0)', 'type == 10')],
    'exp_pr': [('if (__builtin_expect(*pr != 0, 0))', 'if (*pr != 0)')],
    'lab_t5le': [('		t5le: __attribute__((hot));\n', '')],
    'vol_fail': [('	__asm__ __volatile__("");\n', '')],
    'lab_none': [('none: __attribute__((cold));\n', 'none:\n')],
    'pin_size': [('		__asm__("" : "+b"(size));\n', '')],
    'exp_devgl': [('__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0)', 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16')],
}


def off(t, *names):
    for n in names:
        for a, b in H[n]:
            if a not in t:
                raise ValueError('%s: not found: %r' % (n, a[:60]))
            t = t.replace(a, b, 1)
    return t


def main():
    base = bdlib.read_src()
    sets = [s.split(',') for s in sys.argv[1:]] or [[k] for k in H]

    def one(s):
        r = bdrun.score(off(base, *s))
        return s, r
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, sets))
    res.sort(key=lambda x: sum(x[1]['S'].values()))
    for s, r in res:
        print('%-30s S%d L%d %s' % (','.join(s), sum(r['S'].values()), sum(r['L'].values()), 'IDENTICAL' if r['identical'] else ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items())))


if __name__ == '__main__':
    main()
