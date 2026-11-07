"""Attempt 36, pin_size by a switch on the build type (attempt 35's sw_JKR_dR near miss, 92 loose): keep retail as the
switch's default (PRE reaches it before the kit, so the kit sum's operands flip) but give the kit every type above
BUILD_DEVGL16, as src does, with a GNU case range (`case BUILD_DEVKIT ... 0xffffffff:`), so the switch's lowering can
test `> 5` as the reference does.  Case order, range spellings, retail cases listed or default, pin off."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd470 import arms

ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))

KR = {
    'max': ['\tcase BUILD_DEVKIT ... 0xffffffff:\n'],
    'umax': ['\tcase BUILD_DEVKIT ... UINT32_MAX:\n'],
    'r69': ['\tcase BUILD_DEVKIT ... BUILD_TESTKIT16:\n'],
}
RL = {
    'd': ['\tdefault:\n'],
    'l0d': ['\tcase 0:\n\tcase BUILD_RETAIL:\n\tcase BUILD_GLITCH:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n'],
    'ld': ['\tcase BUILD_RETAIL:\n\tcase BUILD_GLITCH:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n\tdefault:\n'],
    'dl': ['\tdefault:\n\tcase BUILD_RETAIL:\n\tcase BUILD_GLITCH:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n'],
}


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    body = {'J': J, 'K': K, 'R': R}
    out = []
    for kn, kl in KR.items():
        for rn, rl in RL.items():
            if kn == 'r69' and rn == 'l0d':
                continue
            labs = {'J': ['\tcase BUILD_JTAG:\n'], 'K': kl, 'R': rl}
            for perm in itertools.permutations('JKR'):
                s = '\tswitch (xb.type) {\n'
                for a in perm:
                    s += ''.join(labs[a]) + ind(body[a]) + '\t\tbreak;\n'
                s += '\t}\n'
                out.append(('%s_%s_%s' % (kn, rn, ''.join(perm)), base[:i] + head + s + tail + base[j:]))
    return out
