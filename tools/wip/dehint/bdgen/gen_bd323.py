"""Attempt 21, the "could not read" log moved into loadBl (after the switch), so the `*pr` test that vrp1's joiner and FSM
threads resolve (loadBlFiles' `if (r)`) exists at loadBl's profile_estimate with its own probability, instead of being
the caller's test whose join is drained by the FSM threads before the joiner copies are made.  loadBlFiles then only
returns -1.  Axes: where fail: goes (its own log, or `goto out` to the test), the test's spelling, the hints kept
(barrier, t5le, `*pr` expect)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

LOG = 'log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, @R@);'
END_OLD = '''		break;
	}
	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''
ENDS = {
    # fail: logs itself
    'own': '''		break;
	}
	if (@T@)
		@LOG@
	return;
fail:
	__asm__ __volatile__("");
	*pr = -1;
	@LOG@
}
''',
    # fail: goes back to the test
    'out': '''		break;
	}
out:
	if (@T@)
		@LOG@
	return;
fail:
	__asm__ __volatile__("");
	*pr = -1;
	goto out;
}
''',
    # fail: before the test, the switch jumps over it
    'over': '''		break;
	}
	goto out;
fail:
	__asm__ __volatile__("");
	*pr = -1;
out:
	if (@T@)
		@LOG@
}
''',
    # early return form
    'ret': '''		break;
	}
out:
	if (!(@T@))
		return;
	@LOG@
	return;
fail:
	__asm__ __volatile__("");
	*pr = -1;
	goto out;
}
''',
}
CALL_OLD = '''		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

int loadConsoleBlFiles(void)'''
CALL_NEW = '''		if (r)
			return -1;
	}
	return 0;
}

int loadConsoleBlFiles(void)'''
TESTS = {'b': ('*pr', '*pr'), 'ne': ('*pr != 0', '*pr')}


def mk(b, end, tst, hints):
    t = bdrun.sub(b, CALL_OLD, CALL_NEW)
    tt, rr = TESTS[tst]
    e = ENDS[end].replace('@LOG@', LOG.replace('@R@', rr)).replace('@T@', tt)
    t = bdrun.sub(t, END_OLD, e)
    if hints:
        t = bdhints.off(t, *hints)
    return t


HS = [(), ('vol_fail',), ('lab_t5le',), ('exp_pr',), ('lab_t5le', 'exp_pr'), ('vol_fail', 'lab_t5le', 'exp_pr')]


def CASES(base):
    out = []
    for end, tst, h in itertools.product(ENDS, TESTS, HS):
        out.append(('%s %s -%s' % (end, tst, ','.join(h)), lambda b, c=(end, tst, h): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
