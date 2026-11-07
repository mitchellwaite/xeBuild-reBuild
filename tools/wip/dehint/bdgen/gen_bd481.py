"""Attempt 36: the JTAG test as an if, then a switch on the rest (kit as a case range up to 0xffffffff, retail the default
or listed), or the JTAG case inside a switch with retail cases listed as ranges.  pin off."""
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
    KL = {'max': '\tcase BUILD_DEVKIT ... 0xffffffff:\n'}
    RLs = {'d': '\tdefault:\n', 'rng': '\tcase 0 ... BUILD_DEVGL16:\n', 'rngd': '\tcase 0 ... BUILD_DEVGL16:\n\tdefault:\n'}
    for rn, rl in RLs.items():
        for perm in ('KR', 'RK'):
            labs = {'K': KL['max'], 'R': rl}
            s = '\tif (xb.type == BUILD_JTAG) {\n' + J + '\t} else {\n\t\tswitch (xb.type) {\n'
            for a in perm:
                s += ind(labs[a] + ind(body[a]) + '\t\tbreak;\n')
            s += '\t\t}\n\t}\n'
            out.append(('ifJ_%s_%s' % (rn, perm), base[:i] + head + s + tail + base[j:]))
    # all in one switch, retail as ranges around JTAG
    RR = {'r2': '\tcase 0 ... BUILD_RETAIL:\n\tcase BUILD_GLITCH ... BUILD_DEVGL16:\n',
          'r2d': '\tdefault:\n\tcase 0 ... BUILD_RETAIL:\n\tcase BUILD_GLITCH ... BUILD_DEVGL16:\n'}
    KK = {'max': '\tcase BUILD_DEVKIT ... 0xffffffff:\n', 'd': '\tdefault:\n'}
    for rn, rl in RR.items():
        for kn, kl in KK.items():
            if rn == 'r2d' and kn == 'd':
                continue
            for perm in itertools.permutations('JKR'):
                labs = {'J': '\tcase BUILD_JTAG:\n', 'K': kl, 'R': rl}
                s = '\tswitch (xb.type) {\n'
                for a in perm:
                    s += labs[a] + ind(body[a]) + '\t\tbreak;\n'
                s += '\t}\n'
                out.append(('sw_%s_%s_%s' % (rn, kn, ''.join(perm)), base[:i] + head + s + tail + base[j:]))
    return out
