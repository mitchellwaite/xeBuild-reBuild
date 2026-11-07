"""Attempt 45: loadBlFiles written like loadConsoleBlFiles (switch in the loop, r a loop-body local, one -1 site, r tested
once after the switch), built from src's current arms (a45lib.loop).  Axes: fallback, fail site, tail, case 6 first, and
the hint set (all on, all off, each off alone).  `python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd560.py -n 400`."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a45lib import loop

FOCUS = None
HINTS = ['exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'etype', 'cp']


def CASES(base):
    out = []
    for fb, fail, tail, c6 in itertools.product(['src', 'and9', 'con2'], ['c2', 'c23', 'each'], ['src', 'plain', 'and'],
                                                [False, True]):
        if fail == 'each' and tail == 'src':
            pass
        have = [h for h in HINTS if not (h in ('exp_pr', 'lab_t5le') and tail != 'src') and
                not (h == 'vol_fail' and fail == 'each')]
        sets = [(), tuple(have)] + [(h,) for h in have]
        for s in sets:
            lab = '%s %s %s %s|%s' % (fb, fail, tail, 'c6' if c6 else '-', '+'.join(s) or 'none')
            if s == tuple(have) and len(s) > 1:
                lab = lab.split('|')[0] + '|ALLOFF'
            out.append((lab, lambda t, kw=dict(fb=fb, fail=fail, tail=tail, c6=c6, off=s): loop(t, **kw)))
    return out
