"""fl4g.py: at fl4f's base: dead-test subsets and small arms; then natural axes of fl4d alone."""
import itertools, sys
import fllib as L, fl4lib as F, fl4d as D, fl4f as B


def mk(tests=None, **kw):
    return L.sub(F.gen(tests or {}, ('files',), **kw), D.FOR, B.FORM)


if __name__ == '__main__':
    mode = sys.argv[1]
    V = {}
    if mode == 'sub':
        for r in range(0, 8):
            for c in itertools.combinations(F.SITES, r):
                lab = ','.join(c)
                V[lab] = mk(F.st(lab))
        for r in (1, 2):
            for c in itertools.combinations(F.SITES, r):
                for ks in itertools.product((1, 2, 3, 4), repeat=r):
                    lab = ','.join('%s=%d' % x for x in zip(c, ks))
                    V[lab] = mk(F.st(lab))
    elif mode == 'ax':
        for a in D.ORDER:
            if a == 'w':
                continue
            for v in D.AX[a]:
                V[D.lab({a: v})] = D.gen({a: v}, B.BASE)
    print(len(V))
    F.run(V, 'g', show=25)
