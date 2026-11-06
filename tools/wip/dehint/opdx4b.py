"""Attempt 4: dx replaced by dz3 = new dummy label (+ unreachable) with a rev feed (like dz1's /
dz2's) and optionally an asm goto from applyIniOptions' xellbutton code.  Base build/op/nodx.c.
python tools/wip/dehint/opdx4b.py [-k]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opdx4

C = '__builtin_constant_p(xb.blSuffix[1] + %d)'
E0 = '__builtin_expect(' + C + ', 0)'
E1 = '__builtin_expect(' + C + ', 1)'
FEEDS = {
    'c': 'if (%s) goto dz3;' % (C % 31),
    'e0': 'if (%s) goto dz3;' % (E0 % 31),
    'e1': 'if (%s) goto dz3;' % (E1 % 31),
    'ce0': 'if (%s) { if (%s) goto dz3; }' % (C % 31, E0 % 32),
    'e0e0': 'if (%s) { if (%s) goto dz3; }' % (E0 % 31, E0 % 32),
    'e0c': 'if (%s) { if (%s) goto dz3; }' % (E0 % 31, C % 32),
    'cc': 'if (%s) { if (%s) goto dz3; }' % (C % 31, C % 32),
    'e1e0': 'if (%s) { if (%s) goto dz3; }' % (E1 % 31, E0 % 32),
    'e0e1': 'if (%s) { if (%s) goto dz3; }' % (E0 % 31, E1 % 32),
}
DZ2F = '\t\t\tif (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'
DZ1F = '\t\t\tif (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; }\n'


def variants(base):
    out = {}
    for fn, f in FEEDS.items():
        for fp, anchor, after in (('fa', DZ2F, True), ('fm', DZ2F, False), ('fb', DZ1F, False)):
            t0 = base.replace(anchor, anchor + '\t\t\t' + f + '\n' if after else '\t\t\t' + f + '\n' + anchor)
            for pos in ['none', 'log_pre', 'log_post', 'call_post', 'call2_post']:
                t1 = t0 if pos == 'none' else opdx4.ins(t0, pos, 'dz3')
                for dn, g in opdx4.DZ3.items():
                    out['%s:%s:%s:%s' % (fn, fp, pos, dn)] = g(t1)
    return out


def main():
    base = optlib.read_src(os.path.join(optlib.BUILD, 'nodx.c'))
    vs = variants(base)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], optlib.score_text(kv[1])), vs.items()))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for n, r in rs[:int(os.environ.get("TOP", "40"))]:
        print('%-34s %s' % (n, optlib.fmt(r)))
    if '-k' in sys.argv:
        for n, r in rs[:3]:
            open(os.path.join(optlib.BUILD, 'dx4b_%s.c' % n.replace(':', '_')), 'w', newline='\n').write(vs[n])


if __name__ == '__main__':
    main()
