"""fl9e.py <tag> <pass> : pass's SSA replacement table sorted by old version (the order update_ssa inserts PHIs, tree-into-ssa's
old_ssa_names walk), new names that are PHIs in the pass's dump only.  Each new name with the pass that last freed its number and what it was."""
import glob, os, re, sys
import fl9a, fl9b, fllib as L


def table(tag, pas):
    d = os.path.join(L.BD, 'a9', 'iv_' + tag)
    q = fl9b.fn(glob.glob(os.path.join(d, '-.*t.' + pas))[0])
    r = []
    for a, b in re.findall(r'(?m)^([\w.]*_\d+) -> \{ ([^}]*)\}', q):
        r.append((a, b.split()))
    return r, q


def ver(s):
    return int(s.rsplit('_', 1)[1])


if __name__ == '__main__':
    tag, pas = sys.argv[1], sys.argv[2]
    d = os.path.join(L.BD, 'a9', 'iv_' + tag)
    fl9a.D = d
    P = fl9a.all_defs()
    idx = [i for i, p in enumerate(P) if p[1] == pas][0]
    tb, q = table(tag, pas)
    rows = []
    for a, olds in tb:
        rows.append((min(ver(o) for o in olds), a, olds))
    for o, a, olds in sorted(rows, key=lambda r: (r[0], ver(r[1]))):
        n = ver(a)
        last = None
        for i in range(idx - 1, -1, -1):
            if n in P[i][2]:
                last = (P[i][1], P[i + 1][1], P[i][2][n])
                break
        cur = P[idx][2].get(n, '')
        print('%-12s <- %-22s %-44s %s' % (a, ' '.join(olds), cur[:44], ('gone after %s: %s' % (last[0], last[2][:46])) if last else 'new'))
