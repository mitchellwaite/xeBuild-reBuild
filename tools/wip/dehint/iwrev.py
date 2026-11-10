"""Score source variants of image_write.c against build/iw/reference.o (the borderline
review, 2026-11-10; notes/image_write.md, "Review").

python tools/wip/dehint/iwrev.py <variants.py> [label...] [-b base.c] [-o label out.c]

variants.py defines V = [(label, [(old, new), ...]), ...]; each old must occur exactly once
in the text after the earlier replacements. The base defaults to src/image_write.c; the
iwrev_*.py variant files were written against afaa16c3's (`git show
afaa16c3:src/image_write.c > build/iw/rv/a0.c`, then `-b build/iw/rv/a0.c`). Plain -O3, as
build.sh compiles the object. -o writes one variant's source."""
import concurrent.futures as cf
import os
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib  # noqa: E402


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
    out = None
    base = os.path.join(R, 'src', 'image_write.c')
    if '-o' in a:
        i = a.index('-o')
        out = (a[i + 1], a[i + 2])
        del a[i:i + 3]
    if '-b' in a:
        i = a.index('-b')
        base = a[i + 1]
        del a[i:i + 2]
    src = read(base)
    V = [v for v in ns['V'] if not a or v[0] in a]
    texts = {}
    for lab, reps in V:
        try:
            texts[lab] = apply(src, reps)
        except ValueError as e:
            print('%-12s BAD %s' % (lab, e))
    if out:
        open(out[1], 'w', newline='\n').write(texts[out[0]])
    with cf.ThreadPoolExecutor(6) as ex:
        res = {lab: ex.submit(iwlib.score_text, t, []) for lab, t in texts.items()}
        for lab in texts:
            print('%-12s %s' % (lab, iwlib.fmt(res[lab].result())), flush=True)


main()
