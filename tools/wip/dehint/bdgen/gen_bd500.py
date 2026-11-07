"""Attempt 38: pin_size, live statements at retail's start (attempt 37's route: retail's first block must not be its
findFileOffset(5) loop header at ch2, without a source-level load that becomes a loop bound), plus the shared
setPatchSlot / imgCfSize tail of the kit and retail arms (block numbering).  pin off.
Run: python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd500.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd470 import arms

SUMS = ('\t\tsize = findFileOffset(5) + findFileSize(5);\n\t\tsize += findFileSize(6);\n'
        '\t\tsize += findFileSize(7);\n\t\tsize += findFileSize(8);\n')
TAIL = '\t\tsetPatchSlot(size);\n\t\tsize += 2 * imgCfSize();\n'
ALIGN = '\t\tsize = (size + 0xffff) & ~0xffff;\n'
X0 = '\t\tif (xb.type != BUILD_RETAIL) {\n\t\t\tx = findFile(25);\n\t\t\tif (xb.files[x].offset > size) {\n'


def ind(s):
    return ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    assert R.startswith(SUMS) and R.endswith(TAIL) and K.endswith(TAIL)
    xell = R[len(SUMS):-len(TAIL)]
    assert xell.startswith(X0) and xell.endswith(ALIGN)
    blk = xell[:-len(ALIGN)]
    inner = blk[len(X0):]
    assert inner.endswith('\t\t\t}\n\t\t}\n')
    flat = ''.join(l[1:] if l.startswith('\t\t\t') else l for l in inner[:-len('\t\t}\n')].splitlines(True))
    V = {'src': (J, K, R)}
    # the xell lookup first (live: x is used by the offset test), so retail starts with the type test
    pre = '\t\tx = 0;\n\t\tif (xb.type != BUILD_RETAIL)\n\t\t\tx = findFile(25);\n'
    V['x25_first_and'] = (J, K, pre + SUMS + '\t\tif (xb.type != BUILD_RETAIL && xb.files[x].offset > size) {\n' + flat + ALIGN + TAIL)
    V['x25_first_nest'] = (J, K, pre + SUMS + '\t\tif (xb.type != BUILD_RETAIL) {\n\t\t\tif (xb.files[x].offset > size) {\n' + inner + ALIGN + TAIL)
    V['sum_one_expr'] = (J, K, '\t\tsize = findFileOffset(5) + findFileSize(5) + findFileSize(6) + findFileSize(7) + findFileSize(8);\n' + xell + TAIL)
    out = []
    for k, (j_, k_, r_) in V.items():
        s = '\tif (xb.type == BUILD_JTAG) {\n' + j_ + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + k_ + '\t} else {\n' + r_ + '\t}\n'
        out.append((k, base[:i] + head + s + tail + base[j:]))
    # the kit's and retail's common tail written once, the 5-test nested in an else
    Kb, Rb = K[:-len(TAIL)], R[:-len(TAIL)]
    for nm, s in (('shared_tail_KR', '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else {\n\t\tif (xb.type > BUILD_DEVGL16) {\n' + ind(Kb) +
                   '\t\t} else {\n' + ind(Rb) + '\t\t}\n' + TAIL + '\t}\n'),
                  ('shared_tail_RK', '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else {\n\t\tif (xb.type <= BUILD_DEVGL16) {\n' + ind(Rb) +
                   '\t\t} else {\n' + ind(Kb) + '\t\t}\n' + TAIL + '\t}\n')):
        out.append((nm, base[:i] + head + s + tail + base[j:]))
    return out
