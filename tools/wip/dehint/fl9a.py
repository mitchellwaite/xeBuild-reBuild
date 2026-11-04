"""fl9a.py <tag> [n] [pass]: names first appearing at <pass> (default dom3) in dump tag, in the order they appear,
each with: the last pass that had that number before, and what it was.  Shows the free stack as the pass pops it,
and which pass freed each entry.  Definitions come from every tree dump of build/filelist_ini/dump/<tag>."""
import glob, os, re, sys
import fllib as L

tag = sys.argv[1] if __name__ == '__main__' else ''
N = int(sys.argv[2]) if __name__ == '__main__' and len(sys.argv) > 2 else 45
PASS = sys.argv[3] if __name__ == '__main__' and len(sys.argv) > 3 else 'dom3'
D = os.path.join(L.BD, 'dump', tag)
DEF =re.compile(r'^\s*(?:# )?(?:\w+ = )?(?:# )?([\w.]*_(\d+))(?:\(D\))? = (?:PHI <)?(.*)')


def passes():
    r = []
    for f in glob.glob(os.path.join(D, '-.*t.*')):
        m = re.search(r'\.(\d+)t\.([\w.+-]+)$', f)
        if m:
            r.append((int(m.group(1)), m.group(2), f))
    return sorted(r)


def fn(f, name='parseIni'):
    t = open(f, errors='replace').read()
    for q in re.split(r'(?m)^(?=;; Function )', t):
        if q.startswith(';; Function %s ' % name):
            return q
    return ''


def defs(q):
    d = {}
    for ln in q.splitlines():
        m = DEF.match(ln)
        if m:
            d.setdefault(int(m.group(2)), ln.strip())
    return d


def all_defs():
    return [(n, nm, defs(fn(f))) for n, nm, f in passes()]


if __name__ == '__main__':
    P = all_defs()
    idx = [i for i, p in enumerate(P) if p[1] == PASS][0]
    prev = P[idx - 1][2]
    cur = open(glob.glob(os.path.join(D, '-.*t.' + PASS))[0], errors='replace').read()
    q = fn(glob.glob(os.path.join(D, '-.*t.' + PASS))[0])
    seen = []
    # in dump order; the true pop order is approximated by first appearance in pass: see notes
    for ln in q.splitlines():
        m = DEF.match(ln)
        if m and int(m.group(2)) not in prev and int(m.group(2)) not in seen:
            seen.append(int(m.group(2)))
    for k in seen[:N]:
        last = None
        for i in range(idx - 1, -1, -1):
            if k in P[i][2]:
                last = (P[i][1], P[i][2][k])
                break
        cur_def = P[idx][2][k]
        print('%-34s last in %-12s %s' % (cur_def[:34], last[0] if last else '-', (last[1] if last else '-')[:60]))
