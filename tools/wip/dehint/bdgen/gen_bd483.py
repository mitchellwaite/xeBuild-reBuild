"""Attempt 36: `if (JTAG) J else switch (xb.type) { R's types listed without 2; kit as a range }` with no default: the
labels don't cover the index type contiguously (2 is missing), so the gimplifier's default goes past the switch, and
retail stays a case node of its own (its range ends at 5, the reference's `cmp 5`).  Spellings and orders.  pin off."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd470 import arms

ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    body = {'J': J, 'K': K, 'R': R}
    out = []
    RL = {'r01_35': '\tcase 0 ... BUILD_RETAIL:\n\tcase BUILD_GLITCH ... BUILD_DEVGL16:\n',
          'rlist': '\tcase 0:\n\tcase BUILD_RETAIL:\n\tcase BUILD_GLITCH:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n',
          'rlist1': '\tcase BUILD_RETAIL:\n\tcase BUILD_GLITCH:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n'}
    KL = {'kmax': '\tcase BUILD_DEVKIT ... 0xffffffff:\n', 'k69': '\tcase BUILD_DEVKIT:\n\tcase BUILD_DEVKIT16:\n\tcase BUILD_TESTKIT:\n\tcase BUILD_TESTKIT16:\n'}
    for rn, rl in RL.items():
        for kn, kl in KL.items():
            for perm in ('KR', 'RK'):
                labs = {'K': kl, 'R': rl}
                s = '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else {\n\t\tswitch (xb.type) {\n'
                for a in perm:
                    s += ind(labs[a] + ind(body[a]) + '\t\tbreak;\n')
                s += '\t\t}\n\t}\n'
                out.append(('ifJ_%s_%s_%s' % (rn, kn, perm), base[:i] + head + s + tail + base[j:]))
    return out
