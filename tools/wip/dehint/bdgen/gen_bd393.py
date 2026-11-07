"""Attempt 28, diagnostic: on the near miss with gen_bd390's `u16` SE compare (no dup, 5 loose: only the word compare),
what each remaining loadBl/loadBlFiles hint costs once the copy is gone, singly and in pairs.  Not a candidate (the
word compare isn't the reference's code); it says what would come free with exp_t10.  Runs on src as of f2823155."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd390 as g

NAMES = ['exp_pr', 'lab_t5le', 'pin_d', 'vol_fail', 'exp_devgl', 'pin_size', 'lab_none']


def PRE(b):
    return g.mk(g.PRE(b), 'u16')


def CASES(base):
    out = [('none', lambda b: b)]
    for n in NAMES:
        out.append((n, lambda b, n=n: bdhints.off(b, n)))
    for a, c in itertools.combinations(['exp_pr', 'lab_t5le', 'pin_d', 'vol_fail'], 2):
        out.append((a + '+' + c, lambda b, a=a, c=c: bdhints.off(b, a, c)))
    out.append(('pr+t5le+else', lambda b: bdhints.off(b, 'exp_pr', 'lab_t5le').replace('\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n', 1)))
    out.append(('else', lambda b: bdrun.sub(b, '\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n', 1)))
    return out
