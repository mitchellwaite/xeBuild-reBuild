"""Attempt 18, measurement only: windows of each test (expect at P, steps of 1) with the pin kept and attribute subsets:
is there any band where the attribute's jobs (B and the hoists) go by frequency alone?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir17lib
from ir17lib import base, score
ATT = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
SUB = {'a0': 'void getImageSmc', 'tm': '__attribute__((optimize("no-tree-tail-merge"))) void getImageSmc', 'i1i2': '__attribute__((optimize("no-if-conversion", "no-if-conversion2"))) void getImageSmc',
       'i2tm': '__attribute__((optimize("no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc', 'i1tm': '__attribute__((optimize("no-if-conversion", "no-tree-tail-merge"))) void getImageSmc'}
T = {
 'bad': ('if (bad > 0) {', 'if (__builtin_expect(bad, 1)) {'),
 'ok': ('if (ok <= 0) {', 'if (__builtin_expect(ok <= 0, 1)) {'),
 'wrong': ('if (wrong > 0)', 'if (__builtin_expect(wrong, 1))'),
 't': ('if (t != 0x1000) {', 'if (__builtin_expect(t != 0x1000, 1)) {'),
 'o': ('if (o <= 0) {', 'if (__builtin_expect(o <= 0, 1)) {'),
 'lim': ('if ((unsigned)addr != lim) {', 'if (__builtin_expect((unsigned)addr != lim, 1)) {'),
 'out': ('if (out <= 0) {', 'if (__builtin_expect(out <= 0, 1)) {'),
}
if __name__ == '__main__':
    for sk, s in SUB.items():
        for tk, (a, b) in T.items():
            assert a in base, a
            t = base.replace(ATT, s).replace(a, b)
            run = []
            for p in range(2, 100, 2):
                r = score(t, ('--param', 'builtin-expect-probability=%d' % p))
                run.append('%d:%s/%s' % (p, r[1], r[0]))
            # compress
            best = sorted(run, key=lambda x: int(x.split(':')[1].split('/')[0]))[:6]
            print(sk, tk, ' '.join(best), flush=True)
