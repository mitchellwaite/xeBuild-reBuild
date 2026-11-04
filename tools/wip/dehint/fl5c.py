"""fl5c.py single|rand [N seed] [T..]: attempt 4's natural axes (fl4m small helpers, fl4q forms) at subsets of the four parseIni tests,
not just at none (attempt 4 ran these at no tests only).  Imports the attempt 4 modules against the source they were written for (FL4SRC)."""
import os, random, subprocess, sys
import fllib as L
os.environ.setdefault('FL4SRC', os.path.join(L.BD, 'a5', 'src_c392b614.c'))
import fl5lib as F
if not os.path.exists(os.environ['FL4SRC']):
    t = subprocess.run(['git', 'show', 'c392b614:src/filelist_ini.c'], cwd=L.R, stdout=subprocess.PIPE).stdout
    open(os.environ['FL4SRC'], 'wb').write(t)
import fl4lib as G4, fl4d as D, fl4m as M, fl4q as Q
L.FLAGS[:] = ['-O3']

AX = dict(M.AX)
AX['fail'] = D.AX['fail']
AX['fl'] = {k: (lambda s, v=v: L.sub(s, Q.FL_IF, v)) for k, v in Q.FL.items()}
for e, (o, n) in Q.EDITS.items():
    if e in ('rawlog', 'loopbreak', 'rawend'):
        continue
    AX[e] = {'y': (lambda s, o=o, n=n: L.sub(s, o, n))}
ORDER = list(AX)


def gen(c, t):
    s = F.gen(t)
    for a in ORDER:
        if a in c:
            if a == 'base' and 'tool' in c:
                continue
            s = AX[a][c[a]](s)
    return s


def lab(c, t):
    return ','.join('%s=%s' % (a, c[a]) for a in ORDER if a in c) + '|' + '+'.join(t)


TN = ['raw', 'off3', 'off4', 'x']
if __name__ == '__main__':
    V = {}
    mode = sys.argv[1]
    if mode == 'single':
        import itertools
        subs = [c for r in range(0, 4) for c in itertools.combinations(TN, r)]
        for t in subs:
            V[lab({}, t)] = F.gen(t)
            for a in ORDER:
                for v in AX[a]:
                    try:
                        V[lab({a: v}, t)] = gen({a: v}, t)
                    except (ValueError, AttributeError, AssertionError) as x:
                        sys.stderr.write('skip %s=%s %r\n' % (a, v, str(x)[:70]))
    else:
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        fixed = sys.argv[4].split(',') if len(sys.argv) > 4 else None
        rng = random.Random(seed)
        while len(V) < N:
            c = {}
            for a in ORDER:
                if rng.random() < 0.12:
                    c[a] = rng.choice(list(AX[a]))
            if fixed is not None:
                t = tuple(fixed)
            else:
                t = tuple(rng.sample(TN, rng.choice((1, 2, 2, 3, 3, 3))))
            try:
                V[lab(c, t)] = gen(c, t)
            except (ValueError, AttributeError, AssertionError):
                pass
    print(len(V))
    F.run(V, 'c', show=30)
