"""fl9c.py <tagA> <tagB> [from] [to]: side by side the modelled free stacks (fl9b) of two a9/iv_<tag> dumps."""
import glob, os, sys
import fl9a, fl9b, fllib as L

A = os.path.join(L.BD, 'a9')


def get(t):
    d = os.path.join(A, 'iv_' + t)
    st, d0, d1 = fl9b.model(d)
    dom3 = fl9a.defs(fl9b.fn(glob.glob(os.path.join(d, '-.*t.dom3'))[0]))
    split = fl9a.defs(fl9b.fn(glob.glob(os.path.join(d, '-.*t.split-paths'))[0]))
    return [(j, lp, line, txt, dom3.get(j, '') if j not in split else '<before>') for j, lp, line, txt in reversed(st)]


if __name__ == '__main__':
    a, b = get(sys.argv[1]), get(sys.argv[2])
    lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    hi = int(sys.argv[4]) if len(sys.argv) > 4 else 110
    e = ('', '', '', '', '')
    for i in range(lo, hi):
        x = a[i] if i < len(a) else e
        y = b[i] if i < len(b) else e
        print('%3d %-3s l%-4s %-30s %-34s | %-3s l%-4s %-30s %s' % (i, x[1], x[2], x[3][:30], x[4][:34], y[1], y[2], y[3][:30], y[4][:34]))
