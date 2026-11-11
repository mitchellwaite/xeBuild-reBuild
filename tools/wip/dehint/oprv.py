"""Score source variants of options.c against build/op/reference.o (the borderline review,
2026-11-10; notes/options.md, "Review").

python tools/wip/dehint/oprv.py <variants.py> [label...] [-b base.c] [-o label out.c] [-v label [fn]]

variants.py defines V = [(label, [(old, new), ...]), ...]; each old must occur exactly once
in the text after the earlier replacements.  A label may also be `a+b`: the edits of a,
then those of b.  The base defaults to src/options.c; the oprv_*.py variant files were
written against 98a0eba6's (`git show 98a0eba6:src/options.c > build/op/rv/a0.c`, then
`-b build/op/rv/a0.c`).  Plain -O3, as build.sh compiles the object.  -o writes one
variant's source; -v prints one variant's diff against the reference."""
import concurrent.futures as cf
import os
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib  # noqa: E402


def read(p):
    return open(p, newline='').read().replace('\r\n', '\n')


def apply(src, reps):
    t = src
    for old, new in reps:
        n = t.count(old)
        if n != 1:
            raise ValueError('%d matches for %r' % (n, old[:80]))
        t = t.replace(old, new)
    return t


def main():
    a = sys.argv[1:]
    vpath = a.pop(0)
    ns = {'__file__': os.path.abspath(vpath)}
    exec(open(vpath).read(), ns)
    out = verbose = None
    base = optlib.SRC
    if '-o' in a:
        i = a.index('-o')
        out = (a[i + 1], a[i + 2])
        del a[i:i + 3]
    if '-v' in a:
        i = a.index('-v')
        rest = a[i + 1:]
        verbose = (rest[0], rest[1] if len(rest) > 1 else None)
        del a[i:]
    if '-b' in a:
        i = a.index('-b')
        base = a[i + 1]
        del a[i:i + 2]
    src = read(base)
    D = dict(ns['V'])
    labs = a or [v[0] for v in ns['V']]
    if verbose:
        labs = [verbose[0]]
    texts = {}
    for lab in labs:
        try:
            reps = []
            for part in lab.split('+'):
                reps += D[part]
            texts[lab] = apply(src, reps)
        except (ValueError, KeyError) as e:
            print('%-16s BAD %s' % (lab, e))
    if out:
        open(out[1], 'w', newline='\n').write(texts[out[0]])
        return
    if verbose:
        optlib.vdiff(texts[verbose[0]], [], verbose[1])
        return
    with cf.ThreadPoolExecutor(6) as ex:
        res = {lab: ex.submit(optlib.score_text, t, []) for lab, t in texts.items()}
        for lab in texts:
            print('%-16s %s' % (lab, optlib.fmt(res[lab].result())), flush=True)


main()
