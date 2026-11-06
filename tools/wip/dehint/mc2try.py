"""mode_client attempt 2: score hand-written variants of src/mode_client.c (or MCBASE).

python tools/wip/dehint/mc2try.py VARIANTS.py [name ...] [-v name [fn]] [-o name out.c]
VARIANTS.py defines V = {name: [(old, new), ...]}; each old must occur exactly once in the
base (or in the text after the earlier replacements).  Prints mc1lib's report and the trick
count (mc1.count) of each variant."""
import os, runpy, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib


def apply(text, subs):
    for old, new in subs:
        n = text.count(old)
        if n != 1:
            raise ValueError('%d hits for %r' % (n, old[:80]))
        text = text.replace(old, new)
    return text


def main():
    a = sys.argv[1:]
    V = runpy.run_path(a[0])['V']
    base = mc1lib.read_src(mc1.BASE)
    if '-v' in a:
        k = a.index('-v')
        mc1lib.vdiff(apply(base, V[a[k + 1]]), only=a[k + 2] if k + 2 < len(a) else None)
        return
    if '-o' in a:
        k = a.index('-o')
        open(a[k + 2], 'w', newline='\n').write(apply(base, V[a[k + 1]]))
        return
    names = [x for x in a[1:]] or list(V)
    def one(n):
        try:
            t = apply(base, V[n])
        except ValueError as e:
            return n, 'SUBST ' + str(e), 0
        return n, mc1lib.fmt(mc1lib.score_text(t))[:200], mc1.count(t)['total']
    with ThreadPoolExecutor(4) as ex:
        for n, r, c in ex.map(one, names):
            print('%-24s %4d %s' % (n, c, r), flush=True)


if __name__ == '__main__':
    main()
