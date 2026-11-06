"""Attempt 4: replace parseButtonX's dx dummy (6 tricks) with one asm goto in applyIniOptions'
own code to an existing dummy label (dz1/dz2) or a new one (dz3, + unreachable).
Base build/op/nodx.c (opnodx4.py).  python tools/wip/dehint/opdx4.py [-k]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

AG = '__asm__ goto ("" :::: %s);'
LOG = '\t\t\t\tlog_printf(1, "default console DVD eject button is being used to start xell\\n");\n'
SET12 = '\t\t\t\txb.xellButton = 0x12;\n'
CALLX = '\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n'
LOG2 = '\t\t\t\tlog_printf(1, "alternate xell button is disabled\\n");\n'
CALL2 = '\t\t\txb.xellAltButton = parseButton(getIniValue("xellbutton2"));\n'
PATCH = '\t\tOPT("patchsmc", 0x8000000, 0);\n'
DEMON = '\t\tOPT("demon", 8, 0);\n'

# (name, anchor, before?) ; insertion line indented like the anchor
POS = {
    'log_pre': (LOG, True), 'log_post': (LOG, False), 'set_post': (SET12, False),
    'call_pre': (CALLX, True), 'call_post': (CALLX, False),
    'log2_pre': (LOG2, True), 'call2_pre': (CALL2, True), 'call2_post': (CALL2, False),
}
DZ_END = 'dz2:\n\t__builtin_unreachable();\n}'
DZ3 = {
    'dz3_last': lambda t: t.replace(DZ_END, 'dz2:\n\t__builtin_unreachable();\ndz3:\n\t__builtin_unreachable();\n}'),
    'dz3_first': lambda t: t.replace('dz1:\n\t__builtin_unreachable();\n', 'dz3:\n\t__builtin_unreachable();\ndz1:\n\t__builtin_unreachable();\n'),
    'dz3_mid': lambda t: t.replace('dz2:\n\t__builtin_unreachable();\n', 'dz3:\n\t__builtin_unreachable();\ndz2:\n\t__builtin_unreachable();\n'),
}


def ins(t, pos, label):
    a, before = POS[pos]
    assert a in t, pos
    ind = a[:len(a) - len(a.lstrip('\t'))]
    line = ind + AG % label + '\n'
    return t.replace(a, line + a if before else a + line, 1)


def variants(base):
    out = {}
    for pos in POS:
        for lab in ('dz1', 'dz2'):
            out['%s:%s' % (pos, lab)] = ins(base, pos, lab)
        for dn, f in DZ3.items():
            out['%s:%s' % (pos, dn)] = f(ins(base, pos, 'dz3'))
    return out


def main():
    base = optlib.read_src(os.path.join(optlib.BUILD, 'nodx.c'))
    vs = variants(base)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], optlib.score_text(kv[1])), vs.items()))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for n, r in rs:
        print('%-22s %s' % (n, optlib.fmt(r)))
    if '-k' in sys.argv:
        for n, r in rs[:3]:
            open(os.path.join(optlib.BUILD, 'dx4_%s.c' % n.replace(':', '_')), 'w', newline='\n').write(vs[n])


if __name__ == '__main__':
    main()
