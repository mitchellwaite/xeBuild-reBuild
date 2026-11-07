"""Attempt 41, lab_none: where loadConsoleBlFiles tests r.  The `if (r)` exit inside the none test's block (the skip
path then goes straight to the latch at profile_estimate; r is 0 there anyway), r scoped to that block, and the
precheck + label kept or gone.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd531.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd530 import PRECHECK, TAIL

FOCUS = ['_loadConsoleBlFiles']
END = r'''				log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
				break;
			}
		}
		if (r) {
			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
			return -1;
		}
	}
	return 0;
none:'''
IN = r'''				log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
				break;
			}
			if (r) {
				log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
				return -1;
			}
		}
	}
	return 0;
none:'''
HEADR = '''		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;
'''
HEADR_IN = '''		e = &xb.files[i];
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;

			r = 0;
'''


def CASES(base):
    out = []
    for pk in ('plain', 'label'):
        for hk in ('r_top', 'r_in'):
            def f(b, pk=pk, hk=hk):
                i = b.index('int loadConsoleBlFiles(void)')
                head, fn = b[:i], b[i:]
                fn = bdrun.sub(fn, END, IN, 1)
                if hk == 'r_in':
                    fn = bdrun.sub(fn, HEADR, HEADR_IN, 1)
                if pk == 'plain':
                    fn = bdrun.sub(fn, PRECHECK, '', 1)
                    fn = bdrun.sub(fn, TAIL, '\treturn 0;\n}', 1)
                return head + fn
            out.append(('%s %s' % (pk, hk), f))
    return out
