"""Attempt 49: console's case 24 tested ahead of the switch (its arm then gets nonequal's 29%
of the body, not 1/10 of the switch block).  Diagnostic of the frequency direction.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_con3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a49_con import BASE, strip, fn

C24 = '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
PRE = '''			if (type == 24) {
				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
			} else
			switch (type) {'''


def pre(t, keep=False):
    t = strip(t)
    a, b = fn(t)
    f = t[a:b]
    if not keep:
        f = f.replace(C24, '', 1)
    f = f.replace('\t\t\tswitch (type) {', PRE, 1)
    return t[:a] + f + t[b:]


V = {'pre': pre, 'pre_keep': lambda t: pre(t, True)}
