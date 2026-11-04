"""python tools/wip/dehint/iw11p2.py <base.c>: probe (never a candidate): __builtin_expect on `if (partial)` at 50..95 with the inline probe flag: where do imgAddFile's two slots flip, and what else moves?"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
A = '		if (partial) {\n'
assert A in t
t2 = t.replace(A, '		if (__builtin_expect(partial, 1)) {\n')


def one(p):
    r = iwlib.score_text(t2, ['--param', 'builtin-expect-probability=%d' % p, '--param', 'inline-min-speedup=11'])
    return p, r.get('per')


with ThreadPoolExecutor(4) as ex:
    for p, per in ex.map(one, range(50, 96, 3)):
        print(p, per)
