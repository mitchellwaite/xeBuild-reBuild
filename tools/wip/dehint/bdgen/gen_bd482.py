"""Attempt 36: `if (JTAG) J else switch (xb.type) { case 0 ... BUILD_DEVGL16: R; case BUILD_DEVKIT ... 0xffffffff: K; }`
with both ranges listed (no default): the decision tree's root is retail's range, so expand emits `cmp 5; jbe R` (the
reference's test) and jumps to the kit.  Arm order, default placement, range spellings.  pin off."""
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
    RL = {'r05': '\tcase 0 ... BUILD_DEVGL16:\n', 'r05d': '\tdefault:\n\tcase 0 ... BUILD_DEVGL16:\n',
          'r05d2': '\tcase 0 ... BUILD_DEVGL16:\n\tdefault:\n'}
    KL = {'kmax': '\tcase BUILD_DEVKIT ... 0xffffffff:\n', 'kmaxd': '\tcase BUILD_DEVKIT ... 0xffffffff:\n\tdefault:\n'}
    for rn, rl in RL.items():
        for kn, kl in KL.items():
            if 'd' in rn[3:] and kn == 'kmaxd':
                continue
            for perm in ('KR', 'RK'):
                labs = {'K': kl, 'R': rl}
                for outer in ('else', 'elseif'):
                    s = '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else {\n\t\tswitch (xb.type) {\n'
                    for a in perm:
                        s += ind(labs[a] + ind(body[a]) + '\t\tbreak;\n')
                    s += '\t\t}\n\t}\n'
                    if outer == 'elseif':
                        # the switch first, JTAG as the switch's own case
                        s = '\tswitch (xb.type) {\n\tcase BUILD_JTAG:\n' + ind(J) + '\t\tbreak;\n'
                        rr = rl.replace('case 0 ... BUILD_DEVGL16:', 'case 0 ... BUILD_RETAIL:\n\tcase BUILD_GLITCH ... BUILD_DEVGL16:')
                        labs2 = {'K': kl, 'R': rr}
                        for a in perm:
                            s += labs2[a] + ind(body[a]) + '\t\tbreak;\n'
                        s += '\t}\n'
                    out.append(('%s_%s_%s_%s' % (outer, rn, kn, perm), base[:i] + head + s + tail + base[j:]))
    return out
