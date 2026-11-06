"""Attempt 4: control flow inside the existing dead feeds (a `return`, fewer tests) as a lever,
alone and together with single trick removals (optricks names).  Base: src/options.c or OPBASE.

python tools/wip/dehint/opret4.py m            every M edit alone
python tools/wip/dehint/opret4.py mr [R..]     every M edit x every removal R (default list)
python tools/wip/dehint/opret4.py mm           pairs of M edits
python tools/wip/dehint/opret4.py show m1,m2,r1 [-o out.c]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

C = lambda n: '__builtin_constant_p(xb.blSuffix[1] + %d)' % n
E0 = lambda n: '__builtin_expect(%s, 0)' % C(n)
F1 = 'if (%s) { if (%s) goto dz1; return; }' % (C(1), E0(2))
F2 = 'if (%s) { if (%s) goto dz2; }' % (E0(15), E0(16))
ZC = lambda n: '__builtin_constant_p(xb.xellButton + %d)' % n
FZ = 'if (%s) { if (%s) goto z; if (%s) goto z; }' % (ZC(1), ZC(2), ZC(3))

M = {
    # dz2's feed
    'f2_ret': (F2, 'if (%s) { if (%s) goto dz2; return; }' % (E0(15), E0(16))),
    'f2_c_in': (F2, 'if (%s) { if (%s) goto dz2; }' % (E0(15), C(16))),
    'f2_c_out': (F2, 'if (%s) { if (%s) goto dz2; }' % (C(15), E0(16))),
    'f2_one': (F2, 'if (%s) goto dz2;' % E0(15)),
    'f2_c_in_ret': (F2, 'if (%s) { if (%s) goto dz2; return; }' % (E0(15), C(16))),
    'f2_c_out_ret': (F2, 'if (%s) { if (%s) goto dz2; return; }' % (C(15), E0(16))),
    'f2_one_ret': (F2, 'if (%s) { goto dz2; }' % E0(15)),
    'f2_cc_ret': (F2, 'if (%s) { if (%s) goto dz2; return; }' % (C(15), C(16))),
    'f2_ret_g1': (F2, 'if (%s) { if (%s) goto dz2; goto dz1; }' % (E0(15), E0(16))),
    # dz1's feed
    'f1_c_in': (F1, 'if (%s) { if (%s) goto dz1; return; }' % (C(1), C(2))),
    'f1_one': (F1, 'if (%s) { goto dz1; }' % C(1)),
    'f1_one_e': (F1, 'if (%s) goto dz1;' % E0(1)),
    'f1_ret_first': (F1, 'if (%s) { if (%s) return; goto dz1; }' % (C(1), E0(2))),
    'f1_ret_c': (F1, 'if (%s) { if (%s) return; goto dz1; }' % (C(1), C(2))),
    'f1_g2': (F1, 'if (%s) { if (%s) goto dz1; goto dz2; }' % (C(1), E0(2))),
    # parseButtonX's z feed
    'z_ret': (FZ, 'if (%s) { if (%s) goto z; return b; }' % (ZC(1), ZC(2))),
    'z_ret0': (FZ, 'if (%s) { if (%s) goto z; return 0; }' % (ZC(1), ZC(2))),
    'z_one': (FZ, 'if (%s) goto z;' % ZC(1)),
    'z_two': (FZ, 'if (%s) { if (%s) goto z; }' % (ZC(1), ZC(2))),
    'z_two_ret': (FZ, 'if (%s) { if (%s) goto z; return 0x11; }' % (ZC(1), ZC(2))),
    'z_ret1': (FZ, 'if (%s) { goto z; }' % ZC(1)),
}
R = ['mG_cygnos', 'mG_smcne', 'mG_nosec', 'mG_nandmu', 'G_exp', 'N_exp', 'N_entry4', 'm_N', 'bx_z',
     'bx_exp', 'pb_exp', 'G_cp1', 'G_cp2', 'N_cp2', 'ib_cp1', 'ib_cp2', 'mac_ms4', 'mac_goto4',
     'dual_goto4', 'po_exp2', 'part']


def apply_m(t, names):
    for n in names:
        a, b = M[n]
        if a not in t:
            return None
        t = t.replace(a, b, 1)
    return t


def build(names, base):
    ms = [n for n in names if n in M]
    rs = [n for n in names if n not in M]
    t = apply_m(base, ms)
    if t is None:
        return None
    t, got = optricks.apply(t, rs)
    if len(got) != len(rs):
        return None
    return t


def score(names, base):
    t = build(names, base)
    if t is None:
        return {'compile': 'not applicable'}
    return optlib.score_text(t, optricks.flags_for(names))


def run(combos, base):
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda c: (c, score(list(c), base)), combos))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for c, r in rs[:int(os.environ.get('TOP', '40'))]:
        print('%-36s %s' % ('+'.join(c), optlib.fmt(r)), flush=True)


def main():
    a = sys.argv[1:]
    cmd = a.pop(0)
    base = optricks.base()
    if cmd == 'm':
        run([(n,) for n in M], base)
    elif cmd == 'mm':
        run(list(itertools.combinations(M, 2)), base)
    elif cmd == 'mr':
        run([(m, r) for m in M for r in (a or R)], base)
    elif cmd == 'show':
        names = a.pop(0).split(',')
        t = build(names, base)
        if '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(t)
        print(optlib.fmt(optlib.score_text(t, optricks.flags_for(names))))


if __name__ == '__main__':
    main()
