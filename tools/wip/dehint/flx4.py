"""flx4.py: helpers over flx3: show a labelled state's diff; hill-climb from a state over all axes.
  flx4.py diff  'nest|dead+dead|ax=v,ax=v'
  flx4.py hill  'nest|dead+dead|ax=v,ax=v' [rounds]   (one-axis changes, plus dropping or adding one dead test)
"""
import difflib, os, sys, itertools
import fllib as L, flx as X, flx3 as A


def parse(lbl):
    fl, d, c = lbl.split('|')
    dead = [x for x in d.split('+') if x]
    ch = dict(kv.split('=') for kv in c.split(',') if kv)
    return fl, dead, ch


def src(fl, dead, ch):
    return A.apply(X.gen(dead, fl), ch)


def lab(fl, dead, ch):
    return A.label(dead, fl, ch)


def tricks(fl, dead):
    return 8 - len(dead) + (1 if fl != 'nest' else 0)


def neighbours(fl, dead, ch):
    out = {}
    for ax in A.AXES:
        for v in list(A.AXES[ax]) + [None]:
            if ch.get(ax) == v:
                continue
            c = dict(ch)
            if v is None:
                c.pop(ax)
            else:
                c[ax] = v
            out[lab(fl, dead, c)] = (fl, dead, c)
    for d in X.ALLDEAD:
        dd = [x for x in X.ALLDEAD if (x in dead) != (x == d)]
        out[lab(fl, dd, ch)] = (fl, dd, ch)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    st = parse(sys.argv[2])
    if cmd == 'diff':
        o = L.compile(src(*st), None, 'dd')
        print(L.score(o)[:4])
        for ln in difflib.unified_diff(L.dis(L.REF)['_parseIni'], L.dis(o)['_parseIni'], lineterm='', n=int(os.environ.get('CTX', 2))):
            print(ln)
    elif cmd == 'save':
        open(sys.argv[3], 'w', newline='\n').write(src(*st))
    else:
        rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        seen = {}
        cur = st
        best = L.score(L.compile(src(*cur), None, 'h'))[0]
        print('start', best, lab(*cur))
        for r in range(rounds):
            V, meta = {}, {}
            for n, m in neighbours(*cur).items():
                if n in seen:
                    continue
                try:
                    V[n] = src(*m)
                    meta[n] = m
                except ValueError:
                    pass
            rs = L.sweep(V, prefix='h', show=0)
            for n, q in rs:
                seen[n] = q[0]
            rs = [(n, q) for n, q in rs if q[0] < 10**6]
            rs.sort(key=lambda x: (x[1][0], tricks(meta[x[0]][0], meta[x[0]][1])))
            for n, q in rs[:6]:
                print(' ', q[0], tricks(meta[n][0], meta[n][1]), n)
            n, q = rs[0]
            if q[0] > best or (q[0] == best and tricks(meta[n][0], meta[n][1]) >= tricks(cur[0], cur[1])):
                break
            best, cur = q[0], meta[n]
            print('round', r, best, lab(*cur))
        print('final', best, lab(*cur))
