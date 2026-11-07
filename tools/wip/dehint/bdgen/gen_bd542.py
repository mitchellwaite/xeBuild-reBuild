"""Attempt 42: gen_bd502's case 6 through `goto chk` (with the constant_p entry off exp_t10 was free there) on gen_bd540's
src / and9 / c2 / c6 bases, crossed with the cluster removals of the pair sweep (cp, exp_t10, exp_pr, t5le, vol_fail).
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd542.py -n 1000 -f _loadBlFiles`."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd540 import BASES, offs

FOCUS = ['_loadBlFiles']
OLD = '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr)
			*pr = checkBl(e->data, e->size, 6, e->crc);
		break;
'''
NEW = '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr)
			break;
		goto chk;
'''
SETS = [('cp',), ('cp', 'exp_t10'), ('cp', 'exp_t10', 'exp_pr'), ('cp', 'exp_t10', 'lab_t5le'),
        ('cp', 'exp_t10', 'exp_pr', 'lab_t5le'), ('cp', 'exp_t10', 'vol_fail'), ('cp', 'exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail')]


def CASES(base):
    out = []
    for b in ('src', 'and9', 'c2', 'c6'):
        for s in SETS:
            if b == 'c6' and 'vol_fail' not in s:
                s = s + ('vol_fail',)
            out.append(('%s|%s' % (b, '+'.join(s)), lambda t, b=b, s=s: offs(bdrun.sub(BASES[b](t), OLD, NEW, 1), s)))
    return out
