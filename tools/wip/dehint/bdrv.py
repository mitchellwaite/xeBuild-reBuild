"""Score source variants of build.c against build/bd/reference.o (the borderline review,
2026-11-10; notes/build.md, "Review").

python tools/wip/dehint/bdrv.py <variants.py> [label...] [-b base.c] [-o label out.c] [-v label [fn]]

variants.py defines V = [(label, [(old, new), ...]), ...]; each old must occur exactly once
in the text after the earlier replacements.  A label may also be `a+b`: the edits of a,
then those of b.  The base defaults to src/build.c; the bdrv_*.py variant files were
written against 46fb4f14's (`git show 46fb4f14:src/build.c > build/bd/rv/a0.c`, then
`-b build/bd/rv/a0.c`).  Plain -O3, as build.sh compiles the object (bdlib).  -o writes one
variant's source; -v prints one variant's diff against the reference."""
import concurrent.futures as cf
import difflib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib  # noqa: E402


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


INC = os.path.join(bdlib.BUILD, 'rv', 'inc')


def headers(lab, reps):
    """edits given as (header, old, new) go to a copy of src/<header> in
    build/bd/rv/inc/<label>/, which is searched before src/; returns the extra flags"""
    hs = {}
    for r in reps:
        if len(r) == 3:
            hs.setdefault(r[0], []).append(r[1:])
    if not hs:
        return []
    d = os.path.join(INC, lab.replace('+', '_'))
    os.makedirs(d, exist_ok=True)
    for h, hr in hs.items():
        t = apply(read(os.path.join(bdlib.R, 'src', h)), hr)
        open(os.path.join(d, h), 'w', newline='\n').write(t)
    return ['-I' + d]


def vdiff(text, only=None, extra=()):
    ok, o, d = bdlib.compile_src(text, extra=extra)
    if not ok:
        print('COMPILE ERROR', o)
        return
    idn, tot, per, notes = bdlib.report(o)
    print('IDENTICAL ' + ' '.join(notes) if idn else '%d %s %s' % (tot, per, ' '.join(notes)))
    fns, _ = bdlib.disasm(o)
    r = bdlib.ref()
    for n in per:
        if only and n != only:
            continue
        if n in fns and n in r['fns']:
            print('=====', n, '(- reference, + draft)')
            for l in difflib.unified_diff(bdlib.norm(r['fns'][n]), bdlib.norm(fns[n]),
                                          lineterm='', n=2):
                if not l.startswith(('---', '+++')):
                    print(l)
    bdlib.cleanup(d)


def main():
    a = sys.argv[1:]
    vpath = a.pop(0)
    # HERE: this directory, for variant files that build on another (exec(open(..)))
    ns = {'__file__': os.path.abspath(vpath), 'HERE': os.path.dirname(os.path.abspath(__file__))}
    exec(open(vpath).read(), ns)
    out = verbose = None
    base = bdlib.SRC
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
    if out:
        labs = [out[0]]
    texts = {}
    extras = {}
    for lab in labs:
        try:
            reps = []
            for part in lab.split('+'):
                reps += D[part]
            texts[lab] = apply(src, [r for r in reps if len(r) == 2])
            extras[lab] = headers(lab, reps)
        except (ValueError, KeyError) as e:
            print('%-16s BAD %s' % (lab, e))
    if out:
        open(out[1], 'w', newline='\n').write(texts[out[0]])
        return
    if verbose:
        vdiff(texts[verbose[0]], verbose[1], extras[verbose[0]])
        return
    with cf.ThreadPoolExecutor(6) as ex:
        res = {lab: ex.submit(bdlib.score_text, t, bdlib.P98, None, extras[lab])
               for lab, t in texts.items()}
        for lab in texts:
            print('%-16s %s' % (lab, bdlib.fmt(res[lab].result())), flush=True)


main()
