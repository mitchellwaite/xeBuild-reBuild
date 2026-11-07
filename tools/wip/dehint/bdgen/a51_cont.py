"""Attempt 51: console's case 24 guard as `if (!xb.glitch2mfg) continue;` (r is 0 there, so skipping the
r test changes nothing): PRED_CONTINUE on the skip path with the call heuristic gives the guard
about 34% (window for lab_none: 35.1% to 38.5%, a51 notes), crossed with loadBl24 bodies.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_cont.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub
import a50_bl24 as B

BASE = H.BASE
OLD = '''				if (xb.glitch2mfg)
					r = loadBl24(e);
				break;
			case 25:'''
G = {
    'c1': '''				if (!xb.glitch2mfg)
					continue;
				r = loadBl24(e);
				break;
			case 25:''',
    'c2': '''				if (xb.glitch2mfg) {
					r = loadBl24(e);
					break;
				}
				continue;
			case 25:''',
}
V = {}
for b in os.environ.get('A51_B', 'src,or,ok1,n2').split(','):
    for g, c in G.items():
        for none in (0, 1):
            def f(t, b=b, c=c, none=none):
                t = sub(t, B.OLD, B.BODIES[b])
                t = sub(t, OLD, c)
                if none:
                    t = sub(t, *H.NONE)
                    t = sub(t, *H.NONE2)
                return t
            V['%s_%s_%s' % (b, g, 'N' if none else 'k')] = f
