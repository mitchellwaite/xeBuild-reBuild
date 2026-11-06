"""Attempt 4: dz3's feed shares the outer test of dz1's or dz2's rev feed (inner test only).
dz3 = asm goto at ASMPOS (opdx4.POS) + label/unreachable after dz2.  Base build/op/nodx.c.
python tools/wip/dehint/opdx4e.py [-k]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opdx4

C = '__builtin_constant_p(xb.blSuffix[1] + %d)'
IN = {'c': 'if (%s) goto dz3;' % (C % 3),
      'e0': 'if (__builtin_expect(%s, 0)) goto dz3;' % (C % 3),
      'e1': 'if (__builtin_expect(%s, 1)) goto dz3;' % (C % 3),
      'g': 'goto dz3;'}
D1 = 'if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; }'
D2 = 'if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }'


def variants(base):
    out = {}
    for asmpos in ('log_pre', 'log_post', 'set_post'):
        t0 = opdx4.DZ3['dz3_last'](opdx4.ins(base, asmpos, 'dz3'))
        for nm, d in (('d1', D1), ('d2', D2)):
            assert d in t0
            for inn, f in IN.items():
                out['%s:%s:after:%s' % (asmpos, nm, inn)] = t0.replace(d, d[:-1] + ' ' + f + ' }')
                k = d.index('{ ') + 2
                out['%s:%s:before:%s' % (asmpos, nm, inn)] = t0.replace(d, d[:k] + f + ' ' + d[k:])
    return out


def main():
    base = optlib.read_src(os.path.join(optlib.BUILD, 'nodx.c'))
    vs = variants(base)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], optlib.score_text(kv[1])), vs.items()))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for n, r in rs[:int(os.environ.get('TOP', '30'))]:
        print('%-28s %s' % (n, optlib.fmt(r)))
    if '-k' in sys.argv:
        for n, r in rs[:2]:
            open(os.path.join(optlib.BUILD, 'dx4e_%s.c' % n.replace(':', '_')), 'w', newline='\n').write(vs[n])


if __name__ == '__main__':
    main()
