"""fl4h.py <secs +list> [n]: fl4f base + section helpers: normalised diff of parseIni."""
import difflib, sys
import fllib as L, fl4lib as F, fl4d as D, fl4f as B


def mk(secs, tests=None):
    return L.sub(F.gen(tests or {}, ('files',) + tuple(secs)), D.FOR, B.FORM)


if __name__ == '__main__':
    o = L.compile(mk(sys.argv[1].split('+') if sys.argv[1] else []), None, 'a4h')
    print(F.nscore(o), F.vec(o), L.score(o)[2:])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    a, b = F.norm(L.dis(L.REF)), F.norm(L.dis(o))
    for k in a:
        if a[k] != b.get(k):
            print('==', k, len(a[k]), len(b.get(k, [])))
            for ln in list(difflib.unified_diff(a[k], b.get(k, []), lineterm='', n=1))[:n]:
                print(ln)
