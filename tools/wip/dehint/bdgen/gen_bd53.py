"""loadBl: each `break` written `return` (and all of them), with each hint off alone."""
from bdone import infn, fnspan

HEAD = 'static void loadBl('
OFFS = ['', 'exp_t10', 'lab_t5le', 'exp_pr', 'lab_t5le,exp_pr', 'lab_badsize', 'lab_t5le,exp_pr,lab_badsize', 'exp_27', 'pin_d', 'vol_fail']


def CASES(base):
    a, b = fnspan(base, HEAD)
    n = base[a:b].count('break;')
    out = []
    for off in OFFS:
        if off:
            out.append((off, 'all', infn(HEAD, 'break;', 'return;')))
        for i in range(n):
            out.append((off, 'b%d' % i, infn(HEAD, 'break;', 'return;', i)))
    return out
