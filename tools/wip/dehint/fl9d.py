"""fl9d.py <tag> <n> [n..]: history of SSA numbers in a9/iv_<tag>'s dumps: each pass where the number's definition changes."""
import glob, os, re, sys
import fl9a, fl9b, fllib as L


def history(tag, nums):
    d = os.path.join(L.BD, 'a9', 'iv_' + tag)
    fl9a.D = d
    P = fl9a.all_defs()
    out = {}
    for n in nums:
        last = None
        r = []
        for pn, nm, ds in P:
            cur = ds.get(n)
            if cur != last:
                r.append((pn, nm, cur))
                last = cur
        out[n] = r
    return out


if __name__ == '__main__':
    tag = sys.argv[1]
    h = history(tag, [int(x) for x in sys.argv[2:]])
    for n, r in h.items():
        print('==', n)
        for pn, nm, cur in r:
            print('  %3d %-16s %s' % (pn, nm, (cur or '-')[:90]))
