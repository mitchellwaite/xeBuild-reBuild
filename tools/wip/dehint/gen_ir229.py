"""Attempt 17: in_out_gt (gen_ir228) left only prephitmp's name above lim's (cmp order, order of the 3000 arm's moves): spellings that move PRE's pops."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir227 import *
SAN = 'loadSmc(addr, size); return;'
def sane(ax):
    limk, ak, ik, outk = ax
    lim = {'loc': f'unsigned lim = {LIM};', 'int': f'int lim = {LIM};', 'pg': f'unsigned pg = xb.dumpPages, lim = 528 * pg;'}[limk]
    A, Adecl = {'c': ('(unsigned)addr', ''), 'a': ('a', 'unsigned a = addr;'), 'i': ('addr', ''), 'ca': ('(unsigned)addr', 'unsigned a = addr;')}[ak]
    out = {'o': f'int out = {A} >= lim;', 'n': f'int out = {A} < lim; out = !out;', 'u': f'unsigned out = {A} >= lim;', 'x': f'int in = {A} < lim; int out = !in;', 'y': f'int out = 0; if ({A} >= lim) out = 1;'}[outk]
    tst = {'le': 'if (out <= 0) { %s }' % SAN, 'gt': 'if (out > 0) goto ns; %s' % SAN}[ik]
    return f'{{ {lim} {Adecl} if ({A} != lim) {{ {out} {tst} }} ns: {NOTSANE} }}' if ik == 'gt' else f'{{ {lim} {Adecl} if ({A} != lim) {{ {out} {tst} }} }}\n {NOTSANE}'
forms = {}
for lk, ak, ik, ok_ in itertools.product(('loc', 'int', 'pg'), ('c', 'a', 'i', 'ca'), ('le', 'gt'), ('o', 'n', 'u', 'x', 'y')):
    k = '.'.join((lk, ak, ik, ok_))
    s = sane((lk, ak, ik, ok_))
    forms[k] = body(s, zset='')
    forms[k + '.oks'] = body(s, zset='ok = 1;')
    forms[k + '.nook'] = body(s, zset='', okdecl='', zt='!addr')
if __name__ == '__main__':
    sweep(forms)
