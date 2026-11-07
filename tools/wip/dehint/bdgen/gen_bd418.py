"""Attempt 30: pin_d (and each other loadBl hint) on the equal bases found this attempt and in attempt 26: src, case 6 first
(gen_bd417 `mv 6@0`, IDENTICAL), default one place up (`mv default@10`, IDENTICAL), and9 + c2 (IDENTICAL), and the two
combined.  Does any hint get cheaper on an equal base?  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd410 as g0
import gen_bd417 as g7

ORD6 = ['5', '6', '24', '1', '22', '25', '3', '4', '23', '27', '2', 'default']


def base(b, k):
    if k in ('c6', 'c2c6'):
        i, j = bdrun.fnspan(b, a30lib.LB)
        h, a, t = g7.arms(b[i:j])
        n = g7.names(a)
        o = ['6'] + [x for x in n if x != '6']
        b = g7.reorder(b, o)
    if k in ('c2', 'c2c6'):
        b = g0.and9c2(b)
    if k == 'cdef':
        i, j = bdrun.fnspan(b, a30lib.LB)
        h, a, t = g7.arms(b[i:j])
        n = g7.names(a)
        o = n[:-2] + ['default', n[-2]]
        b = g7.reorder(b, o)
    return b


OFF = ['', 'pin_d', 'exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'cp', 'etype']


def mk(b, k, off):
    b = base(b, k)
    if off == 'cp':
        return bdrun.sub(b, a30lib.CPBLK, '', 1)
    if off == 'etype':
        return bdrun.sub(b, a30lib.ELSETYPE, '				} else\n', 1)
    if off:
        return bdhints.off(b, off)
    return b


def CASES(b):
    return [('%s %s' % (k, o), lambda b, k=k, o=o: mk(b, k, o)) for k, o in itertools.product(['src', 'c6', 'cdef', 'c2', 'c2c6'], OFF)]


FOCUS = ['_loadBlFiles']
