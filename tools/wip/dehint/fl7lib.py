"""fl7lib: attempt 7's helpers.  KF-free base split round findKey, score lines per getter, save logs in build/filelist_ini/a7/.

fk(body, pre='') -> whole source with `pre` + findKey's definition replaced.
run(V, name): as fl6lib.run but logs to a7.
show(src, fns): diff.
"""
import difflib, os, re, sys
import fllib as L, fl6lib as F

A7 = os.path.join(L.BD, 'a7')
os.makedirs(A7, exist_ok=True)
S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
HEAD, TAIL = S[:A], S[B:]


def fk(body, pre=''):
    return HEAD + pre + body + TAIL


def run(V, name, show_=25):
    F.A6 = A7
    return F.run(V, name, show_)


def diff(src, tag='a7show', full=False):
    o = L.compile(src, None, tag)
    print('==', F.nscore(o), L.score(o)[2:])
    a, b = F.norm(L.dis(L.REF)), F.norm(L.dis(o))
    for k in a:
        if a[k] != b.get(k):
            print('--', k)
            print('\n'.join(l for l in difflib.unified_diff(a[k], b.get(k, []), lineterm='', n=1 if not full else 3) if not l.startswith(('---', '+++'))))
