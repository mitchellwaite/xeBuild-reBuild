"""Attempt 32: `else if (type)` (the dead test on the signature-passed log) with every other hint kept, on src.
Attempt 30's gen_bd415 scored flag and result-variable forms only with all seven loadBl hints off.  Here the
signature block alone is replaced by flag joins (a BOOL / int local, or *pr itself tested again), the passed log
first, a ternary, and nested forms, so only etype's job is asked of them.  Runs on src as of ccf9746b."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun

FOCUS = ['_loadBlFiles']
FAILED = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);'
PASSED = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);'
NOKEY = 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);'
VER = 'cbVerifySig(e->data, xb.pub1bl)'

OLD = '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					FAILED
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					PASSED
			} else
				NOKEY
		}
'''

FORMS = {
    'src': OLD,
    'else': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!VER) {
					FAILED
					*pr = -1;
				} else
					PASSED
			} else
				NOKEY
		}
''',
    'pr_again': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!VER) {
					FAILED
					*pr = -1;
				}
				if (!*pr)
					PASSED
			} else
				NOKEY
		}
''',
    'pr_set': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!VER)
					*pr = -1;
				if (*pr)
					FAILED
				else
					PASSED
			} else
				NOKEY
		}
''',
    'pr_tern': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				*pr = VER ? 0 : -1;
				if (*pr)
					FAILED
				else
					PASSED
			} else
				NOKEY
		}
''',
    'ok_two': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				BOOL ok = VER;

				if (!ok) {
					FAILED
					*pr = -1;
				}
				if (ok)
					PASSED
			} else
				NOKEY
		}
''',
    'ok_two_int': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				int ok = VER;

				if (!ok) {
					FAILED
					*pr = -1;
				}
				if (ok)
					PASSED
			} else
				NOKEY
		}
''',
    'ok_else': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				int ok = VER;

				if (!ok) {
					FAILED
					*pr = -1;
				} else
					PASSED
			} else
				NOKEY
		}
''',
    'ok_passfirst': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				int ok = VER;

				if (ok)
					PASSED
				else {
					FAILED
					*pr = -1;
				}
			} else
				NOKEY
		}
''',
    'ok_top': '''		if (type == 5 || type == 17 || type == 11) {
			int ok = 1;

			if (xb.pub1bl) {
				ok = VER;
				if (!ok) {
					FAILED
					*pr = -1;
				}
			} else
				NOKEY
			if (ok && xb.pub1bl)
				PASSED
		}
''',
    'pr_neg': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!VER) {
					FAILED
					*pr = -1;
				} else if (*pr == 0)
					PASSED
			} else
				NOKEY
		}
''',
    'nokey_first': '''		if (type == 5 || type == 17 || type == 11) {
			if (!xb.pub1bl)
				NOKEY
			else if (!VER) {
				FAILED
				*pr = -1;
			} else
				PASSED
		}
''',
    'pr_again_nk': '''		if (type == 5 || type == 17 || type == 11) {
			if (!xb.pub1bl)
				NOKEY
			else {
				if (!VER) {
					FAILED
					*pr = -1;
				}
				if (!*pr)
					PASSED
			}
		}
''',
    'r_local': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				int r = VER ? 0 : -1;

				if (r) {
					FAILED
					*pr = r;
				} else
					PASSED
			} else
				NOKEY
		}
''',
    'r_local2': '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				int r = 0;

				if (!VER) {
					FAILED
					r = -1;
				}
				if (r)
					*pr = r;
				else
					PASSED
			} else
				NOKEY
		}
''',
}


def fill(s):
    return s.replace('FAILED', FAILED).replace('PASSED', PASSED).replace('NOKEY', NOKEY).replace('VER', VER)


def CASES(base):
    old = fill(OLD)
    out = []
    for k, v in FORMS.items():
        out.append((k, bdrun.sub(base, old, fill(v), 1)))
    return out
