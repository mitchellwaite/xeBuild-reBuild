"""Attempt 4: remove a whole dz dummy (label + unreachable, its feed and its asm goto) and let the
remaining rev feed's dead arm carry control flow (return / goto) instead.  Base src/options.c.
python tools/wip/dehint/opdz4.py"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opret4

C, E0 = opret4.C, opret4.E0
F1, F2 = opret4.F1, opret4.F2
AG1 = '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
MS1 = '\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG2 = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
L1 = 'dz1:\n\t__builtin_unreachable();\n'
L2 = 'dz2:\n\t__builtin_unreachable();\n'
ST = ['', 'return;']


def drop1(t, keep_ms=False):
    t = t.replace(AG1, '').replace(L1, '')
    if not keep_ms:
        t = t.replace(MS1, '')
    return t


def drop2(t):
    return t.replace(AG2, '').replace(L2, '')


def variants(base):
    out = {}
    # dz2 gone: F2 replaced by forms without dz2
    b2 = drop2(base)
    f2alt = {'none': '', 'ret_e': 'if (%s) { return; }' % E0(15), 'ret_ee': 'if (%s) { if (%s) return; }' % (E0(15), E0(16)),
             'ret_ee_r': 'if (%s) { if (%s) return; return; }' % (E0(15), E0(16)),
             'g1_ee': 'if (%s) { if (%s) goto dz1; }' % (E0(15), E0(16)),
             'g1_ee_r': 'if (%s) { if (%s) goto dz1; return; }' % (E0(15), E0(16))}
    f1alt = {'keep': F1, 'noret': 'if (%s) { if (%s) goto dz1; }' % (C(1), E0(2))}
    for (n2, v2), (n1, v1) in itertools.product(f2alt.items(), f1alt.items()):
        out['nodz2:%s:%s' % (n2, n1)] = b2.replace(F2, v2).replace(F1, v1)
    # dz1 gone
    for ms in (False, True):
        b1 = drop1(base, ms)
        f1x = {'none': '', 'ret_c': 'if (%s) { return; }' % C(1),
               'ret_ce': 'if (%s) { if (%s) return; return; }' % (C(1), E0(2)),
               'g2_ce_r': 'if (%s) { if (%s) goto dz2; return; }' % (C(1), E0(2)),
               'g2_ce': 'if (%s) { if (%s) goto dz2; }' % (C(1), E0(2))}
        for n1, v1 in f1x.items():
            out['nodz1%s:%s' % ('ms' if ms else '', n1)] = b1.replace(F1, v1)
    return out


def main():
    base = optlib.read_src(optlib.SRC)
    vs = variants(base)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], optlib.score_text(kv[1])), vs.items()))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for n, r in rs:
        print('%-28s %s' % (n, optlib.fmt(r)))


if __name__ == '__main__':
    main()
