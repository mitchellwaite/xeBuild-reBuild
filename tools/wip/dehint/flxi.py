"""flxi.py: `goto tooLong` with the label straight after the name error's return (all dead subsets)."""
import itertools, os, re
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx7 as T, flxh as H

ERRI = X.PATHERR.replace('\t\t\t\t', '\t\t\t\t\t')
PAT = re.compile(r'(\t\t\t\t\tlog_printf\(0, "\\n        Line: %s\\n", xb.firmware\[i\]\);\n\t\t\t\t\tfree\(buf\);\n(?:\t\t\t\t\tif \(off < -1\)\n\t\t\t\t\t\tbuf\[0\] = 1;\n)?\t\t\t\t\treturn 0;\n)')


def form(s):
    a, b = H.plain_removed(s)
    s = a + '\t\t\tif (len > 1023)\n\t\t\t\tgoto tooLong;\n' + b
    s, c = PAT.subn(lambda m: m.group(1) + 'tooLong:\n\t\t\t\t\t' + ERRI, s)
    assert c == 1
    return s


V = {}
for r in range(len(X.ALLDEAD) + 1):
    for rm in itertools.combinations(X.ALLDEAD, r):
        V['+'.join(x for x in X.ALLDEAD if x not in rm)] = form(X.gen(rm, 'asm'))


def one(kv):
    i, (n, s) = kv
    o = L.compile(s, None, 'ii' + str(i))
    if o is None:
        return 10**7, '', n
    sc = L.score(o)
    v = T.vec(o)
    os.remove(o)
    return sc[0], v, n + ' ' + ','.join(sc[3])


with ThreadPoolExecutor(4) as ex:
    rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
for r in rs[:16]:
    print(r)
