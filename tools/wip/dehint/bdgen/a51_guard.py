"""Attempt 51: console's case 24 guard spelled with an opcode predictor, precheck and cold label off.
bbro reading (a51 notes): the r = 1 block gets a trace-end priority only if the inlined defaultBl60
malloc block starts a round-2 trace, i.e. its frequency >= 0.2 x the entry's 880 = 176; it is
716 (case arm) x guard (29%) x loadBl24's share (70%) = 145.  `> 0` adds opcode-positive to the guard.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_guard.py [-p 0,90,95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub

BASE = H.BASE
OLD = '''				if (xb.glitch2mfg)
					r = loadBl24(e);
				break;
			case 25:'''
G = {
    'src': 'xb.glitch2mfg',
    'gt0': 'xb.glitch2mfg > 0',
    'ge1': 'xb.glitch2mfg >= 1',
    'eq1': 'xb.glitch2mfg == 1',
    'ne0': 'xb.glitch2mfg != 0',
}
OFF = {'all': [], 'none': [H.NONE, H.NONE2], 'nonepr': [H.NONE, H.NONE2, H.PR], 'nonedev': [H.NONE, H.NONE2, H.DEV]}
V = {}
for g, c in G.items():
    for k in os.environ.get('A51_OFF', 'all,none').split(','):
        def f(t, c=c, p=OFF[k]):
            t = sub(t, OLD, OLD.replace('if (xb.glitch2mfg)', 'if (%s)' % c))
            for a, b in p:
                t = sub(t, a, b)
            return t
        V['%s_%s' % (g, k)] = f
