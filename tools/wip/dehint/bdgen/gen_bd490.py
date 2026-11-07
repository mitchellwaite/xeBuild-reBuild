"""Attempt 37: pin_size by retail's first block at ch2 (attempt 36's open route).  If retail's arm starts with a
statement that isn't its findFileOffset(5) loop header, ch2 needs no preheader on the 5-test's retail edge, so the kit's
preheader alone goes right after the test, the kit gets the lower index and PRE walks retail first (kit sum flipped),
while the kit stays the true edge (bbro's winner).  Retail-start variants with src's JKR order.  pin off.
Run: python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd490.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd470 import arms

R0 = '\t\tsize = findFileOffset(5) + findFileSize(5);\n'


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    assert R.startswith(R0)
    rest = R[len(R0):]
    head_n = head.replace('\tuint32_t size, xs, x;\n', '\tuint32_t size, xs, x;\n\tint n;\n')
    V = {
        'src': (head, R),
        'n_unused': (head_n, '\t\tn = xb.nFlashFiles;\n' + R),
        'off_split': (head, '\t\tsize = findFileOffset(5);\n\t\tsize += findFileSize(5);\n' + rest),
        'nfiles_unused': (head_n, '\t\tn = xb.nFiles;\n' + R),
        'xell_flag': (head_n, '\t\tn = xb.type != BUILD_RETAIL;\n' + R.replace('if (xb.type != BUILD_RETAIL) {', 'if (n) {')),
        'xs_const': (head, '\t\txs = 0x40000;\n' + R),
        'n2_unused': (head_n, '\t\tn = xb.nFlashFiles2;\n' + R),
        'size_first': (head, '\t\tsize = findFileSize(5) + findFileOffset(5);\n' + rest),
    }
    sums = R[:R.index('\t\tif (xb.type != BUILD_RETAIL)')]
    after = R[len(sums):]
    ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))
    # the sums are 0 when there are no flash files: the loops' shared guard written out
    V['guard_if'] = (head, '\t\tsize = 0;\n\t\tif (xb.nFlashFiles > 0) {\n' + ind(sums) + '\t\t}\n' + after)
    V['guard_ifelse'] = (head, '\t\tif (xb.nFlashFiles > 0) {\n' + ind(sums) + '\t\t} else\n\t\t\tsize = 0;\n' + after)
    V['type_local'] = (head_n, '\t\tn = xb.type;\n' + sums + after.replace('if (xb.type != BUILD_RETAIL) {', 'if (n != BUILD_RETAIL) {'))
    V['both_loads'] = (head_n.replace('\tint n;\n', '\tint n, m;\n'), '\t\tn = xb.nFlashFiles;\n\t\tm = xb.nFiles;\n' + R)
    # semantics differ for type 0: record only
    V['glitch_ge'] = (head, R.replace('if (xb.type != BUILD_RETAIL) {', 'if (xb.type >= BUILD_GLITCH) {'))
    V['flag_twice'] = (head_n, '\t\tn = xb.type != BUILD_RETAIL;\n' + sums + after.replace('if (xb.type != BUILD_RETAIL) {', 'if (n) {').replace(
        '\t\tsize = (size + 0xffff)', '\t\tif (n)\n\t\t\tsize = (size + 0xffff) & ~0xffff;\n\t\telse\n\t\t\tsize = (size + 0xffff)'))
    out = []
    for k, (h, r) in V.items():
        s = '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + K + '\t} else {\n' + r + '\t}\n'
        out.append((k, base[:i] + h + s + tail + base[j:]))
    s = '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else if (xb.type <= BUILD_DEVGL16) {\n' + '\t\tn = xb.nFiles;\n' + R + '\t} else {\n' + K + '\t}\n'
    out.append(('JRK_nfiles', base[:i] + head_n + s + tail + base[j:]))
    return out
