"""ed5.py TAG : g7b + match features A,B(,D) H F G with a grid over P, then fany over f."""
import sys, os, random, copy, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
from ed4 import strip, fany as _f
import ed4
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc29', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys); ed4.f0 = f0
def edit(S, at=1102):
    R = copy.deepcopy(Rr)
    for x in S: strip(R, x)
    g = R[2]['g']; g[at] = g.get(at, []) + [('push', x, -1000001) for x in S]
    for b, es in g.items():
        g[b] = [('ins', e[1], 49, -1000001) if e[0] == 'ins' and e[2] == 49 else e for e in es]
    return R
if __name__ == '__main__':
    best = []
    for S in [(112, 115), (112, 115, 117), (112, 115, 117, 103), (115, 112, 117, 130)]:
        Rx = edit(S)
        for rx in [('126:125', '117:130'), ('126:125',), ()]:
            hsim.RXEV.clear()
            for it in rx:
                s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
            for p49 in (1, 2, 3, 4):
                for p112 in range(1, p49 + 1):
                    for p115 in range(1, p49 + 1):
                        P = dict(P0); P[49] = p49; P[112] = p112; P[115] = p115
                        for x in S[2:]: P[x] = 1
                        if rx: P[125] = 1
                        if len(rx) == 2: P[130] = 1
                        r = _f(Rx, P, 2)
                        print((r[0], S, rx, p49, p112, p115, r[1]), flush=True)
