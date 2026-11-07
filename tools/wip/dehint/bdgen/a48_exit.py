"""Attempt 48: the tail's r test as a loop exit (PRED_LOOP_EXIT is first-match, 9% / n_exits),
so the SE copy's P(<=5) rises: the tail jumps straight to the could-not-read log (r is already -1
there), a copy of the log in the tail, or the log after the loop with `fail:` in front of it.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a48_exit.py"""
import os, itertools
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
TAIL = 'if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;\n'
LOG = '''		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}'''
LOGBAD = '''		if (r) {
		bad:
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}'''
LOGAFTER = '''		if (r)
			goto bad;
	}
	return 0;
fail:
	r = -1;
bad:
	log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
	return -1;
}'''
FAILBLK = '''			fail:
				__asm__ __volatile__("");
				r = -1;
				break;
'''
FAILBLK_NB = '''			fail:
				r = -1;
				break;
'''
FAILBLK_GONE = '''				r = -1;
				break;
'''
BAR = ('\t\t\t\t__asm__ __volatile__("");\n', '')
DUP = lambda c: ('if (%s) {\n\t\t\t\t\t\tlog_printf(0, "\\n\\n**** could not read %%s (%%i) ****\\n\\n", e->name, r);\n'
                 '\t\t\t\t\t\treturn -1;\n\t\t\t\t\t}\n' % c)
V = {}
for c in ('r', '(int)r < 0', 'r != 0'):
    k = {'r': 'r', '(int)r < 0': 'n', 'r != 0': 'ne'}[c]
    V['bad_' + k] = [(TAIL, 'if (%s)\n\t\t\t\t\t\tgoto bad;\n' % c), (LOG, LOGBAD)]
    V['bad_' + k + '_nb'] = V['bad_' + k] + [BAR]
    V['dup_' + k] = [(TAIL, DUP(c))]
    V['dup_' + k + '_nb'] = V['dup_' + k] + [BAR]
    # log after the loop; fail: in front of it (case 2 then ends with r = -1 via goto)
    V['aft_' + k] = [(TAIL, 'if (%s)\n\t\t\t\t\t\tgoto bad;\n' % c), (LOG, LOGAFTER),
                     (FAILBLK, '\t\t\t\tgoto fail;\n')]
    V['aftf_' + k] = [(TAIL, 'if (%s)\n\t\t\t\t\t\tgoto fail;\n' % c), (LOG, LOGAFTER),
                      (FAILBLK, '\t\t\t\tgoto fail;\n')]
    V['aftk_' + k] = [(TAIL, 'if (%s)\n\t\t\t\t\t\tgoto bad;\n' % c), (LOG, LOGAFTER.replace('fail:\n\tr = -1;\n', '')),
                      (FAILBLK, FAILBLK_NB)]
