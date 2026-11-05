"""python tools/wip/dehint/irfree.py <dumpdir> <from-pass-substr> <to-pass-substr>: SSA names appearing/disappearing pass to pass in an irdump dir, between two
passes, to follow the free list (printed as pass: +new -gone, with base names)."""
import os, re, sys

d, a, b = sys.argv[1:4]
fs = sorted(f for f in os.listdir(d))
ia = [i for i, f in enumerate(fs) if a in f][0]
ib = [i for i, f in enumerate(fs) if b in f][0]


def names(f):
    t = open(os.path.join(d, f), errors='replace').read()
    # take the final function body: after the last line that is just the function's header
    i = t.rfind('\ngetImageSmc ()')
    t = t[i:] if i >= 0 else t
    return set(re.findall(r'\b(?:[A-Za-z.][A-Za-z0-9.]*)?_(\d+)\b', t))


prev = names(fs[ia])
for f in fs[ia + 1:ib + 1]:
    n = names(f)
    if not n:
        continue
    add, gone = n - prev, prev - n
    if add or gone:
        print(f, '+', sorted(add, key=int), '-', sorted(gone, key=int))
    prev = n
