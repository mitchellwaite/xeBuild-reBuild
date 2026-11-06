"""Attempt 3: optIniBoolG's (and optN's) __builtin_expect(!bad, 0): natural shapes of the
ini part with the expect gone (the strings are first expanded in optIniBool, so their .rdata
order doesn't move).

python tools/wip/dehint/opg3.py [G|N]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

INI = 'log_printf(1, "Using %s option (ini file)\\n", name);'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'
CUR = '''		bad = iniBoolInvalid(name);
		if (__builtin_expect(!bad, 0)) {
			if (!getIniBool(name, def))
				return 0;
			%s
		} else {
			%s
			return 0;
		}
''' % (INI, WARN)
S = {
    'plain': CUR.replace('__builtin_expect(!bad, 0)', '!bad'),
    'bad_first': '''		bad = iniBoolInvalid(name);
		if (bad) {
			%s
			return 0;
		}
		if (!getIniBool(name, def))
			return 0;
		%s
''' % (WARN, INI),
    'bad_first_else': '''		bad = iniBoolInvalid(name);
		if (bad) {
			%s
			return 0;
		} else if (!getIniBool(name, def))
			return 0;
		else
			%s
''' % (WARN, INI),
    'nest_get': '''		bad = iniBoolInvalid(name);
		if (!bad) {
			if (getIniBool(name, def))
				%s
			else
				return 0;
		} else {
			%s
			return 0;
		}
''' % (INI, WARN),
    'nest_get_bad': '''		bad = iniBoolInvalid(name);
		if (bad) {
			%s
			return 0;
		} else {
			if (!getIniBool(name, def))
				return 0;
			%s
		}
''' % (WARN, INI),
    'eqnull': CUR.replace('__builtin_expect(!bad, 0)', 'bad == NULL'),
    'inline_call': '''		if (!(bad = iniBoolInvalid(name))) {
			if (!getIniBool(name, def))
				return 0;
			%s
		} else {
			%s
			return 0;
		}
''' % (INI, WARN),
}


def fn_range(t, which):
    head = 'static _Bool optIniBoolG(' if which == 'G' else 'static _Bool optN('
    i = t.index(head)
    return i, t.index('\n}\n', i)


def build(which, n):
    t = optlib.read_src(optlib.SRC)
    i, j = fn_range(t, which)
    f = t[i:j]
    assert CUR in f
    return t[:i] + f.replace(CUR, S[n]) + t[j:]


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'G'
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(lambda n: (n, optlib.fmt(optlib.score_text(build(which, n)))), list(S)):
            print(which, n, r[:160])
