"""Attempt 14: natural spellings of dualboot's "ignored" path (where dz2 is pushed from),
crossed with the dz removals.

python tools/wip/dehint/op14db.py [variants..]   (RMS=none,ag2,dzall)"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op13

RM = dict(op13.RM)
RM['none'] = []
AG2 = op13.AG2
LOG = '\t\t\t\tlog_printf(1, "dualboot setting ignored!\\n");\n'
OLD = '''		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton == xb.dualButton) {
''' + LOG + AG2 + '''				xb.dualButton = 0;
			}
		}
'''
V = {}
V['swap'] = OLD.replace('xb.xellButton == xb.dualButton', 'xb.dualButton == xb.xellButton')
V['local'] = '''		if (!xb.dualButton) {
			b = parseButton(getIniValue("dualboot"));
			if (b == xb.xellButton) {
''' + LOG + AG2 + '''				b = 0;
			}
			xb.dualButton = b;
		}
'''
V['local2'] = '''		if (!xb.dualButton) {
			b = parseButton(getIniValue("dualboot"));
			xb.dualButton = b;
			if (xb.xellButton == b) {
''' + LOG + AG2 + '''				xb.dualButton = 0;
			}
		}
'''
V['else'] = '''		if (!xb.dualButton) {
			b = parseButton(getIniValue("dualboot"));
			if (b == xb.xellButton) {
''' + LOG + AG2 + '''				xb.dualButton = 0;
			} else
				xb.dualButton = b;
		}
'''
V['ne'] = '''		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton != xb.dualButton)
				;
			else {
''' + LOG + AG2 + '''				xb.dualButton = 0;
			}
		}
'''
V['zero1st'] = '''		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton == xb.dualButton) {
				xb.dualButton = 0;
''' + LOG + AG2 + '''			}
		}
'''


def build(v, rm):
    t = optlib.read_src(os.environ.get('OPBASE', optlib.SRC))
    assert OLD in t
    t = t.replace(OLD, V[v], 1)
    decl = '\tchar *s;\n\tint i;\n\n\tOPT("nomobile"'
    t = t.replace(decl, '\tchar *s;\n\tint i, b;\n\n\tOPT("nomobile"', 1)
    for old, new in RM[rm]:
        if old not in t:
            return None
        t = t.replace(old, new, 1)
    return t


def run(c):
    t = build(*c)
    if t is None:
        return c, {'compile': 'edit missing'}
    return c, optlib.score_text(t, optlib.P83)


def main():
    a = sys.argv[1:]
    if a and a[0] == 'show':
        v, _, rm = a[1].partition('+')
        optlib.vdiff(build(v, rm or 'none'), optlib.P83)
        return
    vs = a or list(V)
    rms = os.environ.get('RMS', 'none,ag2,dzall').split(',')
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, [(v, r) for v in vs for r in rms]))
    for (v, r), s in res:
        print('%-8s %-6s %s' % (v, r, optlib.fmt(s)))


if __name__ == '__main__':
    main()
