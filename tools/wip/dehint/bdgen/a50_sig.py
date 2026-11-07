"""Attempt 50: loadBlFiles' signature check as a helper (late-inlined, so a call block at
profile_estimate, attempt 50's reading), several bodies, with exp_pr / the barrier / the label off.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_sig.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import ANCHOR, sub, OFF

BASE = H.BASE
OLD = '''				if (type == 5 || type == 17 || type == 11) {
					if (xb.pub1bl) {
						if (!cbVerifySig(e->data, xb.pub1bl)) {
							log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
							r = -1;
						} else
							log_printf(1, "loaded %s, signature check passed!\\n", e->name);
					} else
						log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
				}
'''
NEW = '''				if (type == 5 || type == 17 || type == 11)
					r = checkBlSig(e);
'''
HEAD = '/* a CB/CF/SB\'s signature, by the 1BL key */\nstatic int checkBlSig(struct fileent *e)\n{\n'
FAIL = '\t\tlog_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
PASS = '\tlog_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
NOKEY = '\t\tlog_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
BODIES = {
    'ret': HEAD + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 0;\n\t}\n\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL +
           '\t\treturn -1;\n\t}\n' + PASS + '\treturn 0;\n}\n\n',
    'var': HEAD + '\tint r = 0;\n\n\tif (xb.pub1bl) {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t' + FAIL +
           '\t\t\tr = -1;\n\t\t} else\n\t' + PASS + '\t} else\n' + NOKEY + '\treturn r;\n}\n\n',
    'ret2': HEAD + '\tif (xb.pub1bl) {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t' + FAIL +
            '\t\t\treturn -1;\n\t\t}\n\t' + PASS + '\t} else\n' + NOKEY + '\treturn 0;\n}\n\n',
}
V = {}
for b, body in BODIES.items():
    for k in os.environ.get('A50_OFF', 'all,pr,bar,lab').split(','):
        def f(t, body=body, p=OFF[k]):
            t = sub(t, OLD, NEW)
            t = sub(t, ANCHOR, body + ANCHOR)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V['%s_%s' % (b, k)] = f
