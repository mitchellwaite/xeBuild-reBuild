"""Attempt 42: the signature test's leaf order (`type == 5 || type == 17 || type == 11`, six orders; the Linux build tests
17, 5, 11) on gen_bd540's src / and9 / c2 bases, crossed with the multi-hint removals that the pair sweep found cheap
(exp_t10 and the constant_p entry together frees exp_pr and t5le).  Attempt 24 swept the orders with single hints only.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd541.py -n 1000 -f _loadBlFiles`."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd540 import BASES, offs

FOCUS = ['_loadBlFiles']
SIG = 'if (type == 5 || type == 17 || type == 11) {'
SETS = [(), ('cp',), ('exp_t10',), ('exp_t10', 'cp'), ('exp_t10', 'cp', 'exp_pr', 'lab_t5le'),
        ('exp_t10', 'cp', 'exp_pr', 'lab_t5le', 'vol_fail')]


def order(t, o):
    return bdrun.sub(t, SIG, 'if (%s) {' % ' || '.join('type == %d' % k for k in o), 1)


def CASES(base):
    out = []
    for b in os.environ.get('BDBASES', 'src,and9,c2').split(','):
        for o in itertools.permutations((5, 17, 11)):
            for s in SETS:
                out.append(('%s %s|%s' % (b, ''.join('%02d' % k for k in o), '+'.join(s) or 'none'),
                            lambda t, b=b, o=o, s=s: offs(order(BASES[b](t), o), s)))
    return out
