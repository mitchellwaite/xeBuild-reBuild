"""flxc.py <label> <line_var[,line_var]> [diff]: show a state + inserted tests (lines as in flx6's list, applied high to low)."""
import difflib, sys
import fllib as L, flx as X, flx3 as A, flx4 as F, flx6 as D


def build(lbl, ins):
    fl, dead, ch = F.parse(lbl)
    s = A.apply(X.gen(dead, fl), ch)
    pts = {s.count('\n', 0, p) + 1: p for p in D.points(s)}
    for it in sorted(ins, key=lambda x: -int(x.split('_')[0])):
        ln, v = it.split('_')
        s = D.insert(s, pts[int(ln)], v)
    return s


if __name__ == '__main__':
    s = build(sys.argv[1], [x for x in sys.argv[2].split(',') if x])
    o = L.compile(s, None, 'xc')
    print(L.score(o)[:4])
    for ln in difflib.unified_diff(L.dis(L.REF)['_parseIni'], L.dis(o)['_parseIni'], lineterm='', n=1):
        print(ln)
