"""Attempt 12: parseOption's two expects through helpers with their own profiles (build's
attempt 67-70 lever: a small static helper holding a call is IPA-inlined, not early-inlined,
and brings its own profile_estimate probabilities into the caller).

python tools/wip/dehint/op12po.py [-p N|-np] [S:V ...]
  S = setBool form, V = vlen tail form ('E' = current expect).  No args: every S x V with
  one side 'E', plus every pair.  OUT=file writes the last combination.
Each line: score and the literal order of (u)nknown, (i)ncomplete, (b)ad."""
import os, re, sys, itertools
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

UNKS = '''"\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val'''
INCS = '''"\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt'''
UNK = 'log_printf(1, ' + UNKS + ');'
INC = 'log_printf(1, ' + INCS + ');'

SB_OLD = '''	if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {
		log_printf(1, "\\n");
		return 1;
	}
'''
V_OLD = '''	if (__builtin_expect(vlen, 0)) {
		''' + UNK + '''
		return 0;
	}
	''' + INC + '''
	return 0;
bad:
'''
ANCHOR = '/* one name[=value] from the command line option string.'

# setBool forms: (helper text or '', replacement of SB_OLD)
S = {
    'E': ('', SB_OLD),
    'P': ('', SB_OLD.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)', 'setBoolOption(opt, val) == 1')),
    # helper with the log, early returns
    'H1': ('''static int boolOption(char *opt, char *val)
{
	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		return 1;
	}
	return 0;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H1u': ('''static uint32_t boolOption(char *opt, char *val)
{
	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		return 1;
	}
	return 0;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H1b': ('''static _Bool boolOption(char *opt, char *val)
{
	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		return 1;
	}
	return 0;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    # helper returns the result, logs on success
    'H2': ('''static int boolOption(char *opt, char *val)
{
	int r = setBoolOption(opt, val);

	if (r == 1)
		log_printf(1, "\\n");
	return r;
}

''', '\tif (boolOption(opt, val) == 1)\n\t\treturn 1;\n'),
    'H2b': ('''static int boolOption(char *opt, char *val)
{
	int r = setBoolOption(opt, val);

	if (r == 1)
		log_printf(1, "\\n");
	return r == 1;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H2c': ('''static int boolOption(char *opt, char *val)
{
	int r = setBoolOption(opt, val);

	if (r)
		log_printf(1, "\\n");
	return r;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H3': ('''static int boolOption(char *opt, char *val)
{
	if (setBoolOption(opt, val) != 1)
		return 0;
	log_printf(1, "\\n");
	return 1;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H4': ('''static int boolOption(char *opt, char *val)
{
	int ok = 0;

	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		ok = 1;
	}
	return ok;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    'H5': ('''static int boolOption(char *opt, char *val)
{
	if (setBoolOption(opt, val)) {
		log_printf(1, "\\n");
		return 1;
	}
	return 0;
}

''', '\tif (boolOption(opt, val))\n\t\treturn 1;\n'),
    # caller form with the call's result kept
    'R1': ('', '\tif (setBoolOption(opt, val) == 1)\n\t\tgoto done;\n'),
}

DONE = '''done:
	log_printf(1, "\\n");
	return 1;
'''

# vlen tails: (helper, replacement of V_OLD)
V = {
    'E': ('', V_OLD),
    'P': ('', V_OLD.replace('__builtin_expect(vlen, 0)', 'vlen')),
    # helpers: unknown/incomplete message
    'U1': ('''static void unknownOption(char *opt, char *val, int vlen)
{
	if (vlen)
		log_printf(1, ''' + UNKS + ''');
	else
		log_printf(1, ''' + INCS + ''');
}

''', '\tunknownOption(opt, val, vlen);\n\treturn 0;\nbad:\n'),
    'U2': ('''static uint32_t unknownOption(char *opt, char *val, int vlen)
{
	if (vlen) {
		log_printf(1, ''' + UNKS + ''');
		return 0;
	}
	log_printf(1, ''' + INCS + ''');
	return 0;
}

''', '\treturn unknownOption(opt, val, vlen);\nbad:\n'),
    'U2v': ('''static void unknownOption(char *opt, char *val, int vlen)
{
	if (vlen) {
		log_printf(1, ''' + UNKS + ''');
		return;
	}
	log_printf(1, ''' + INCS + ''');
}

''', '\tunknownOption(opt, val, vlen);\n\treturn 0;\nbad:\n'),
    'U3': ('''static int unknownOption(char *opt, char *val, int vlen)
{
	if (vlen)
		log_printf(1, ''' + UNKS + ''');
	else
		log_printf(1, ''' + INCS + ''');
	return 0;
}

''', '\treturn unknownOption(opt, val, vlen);\nbad:\n'),
    'U4': ('''static void unknownOption(char *opt, char *val, int vlen)
{
	if (!vlen) {
		log_printf(1, ''' + INCS + ''');
		return;
	}
	log_printf(1, ''' + UNKS + ''');
}

''', '\tunknownOption(opt, val, vlen);\n\treturn 0;\nbad:\n'),
    'U5': ('''static void unknownOption(char *opt, char *val, int vlen)
{
	if (vlen > 0)
		log_printf(1, ''' + UNKS + ''');
	else
		log_printf(1, ''' + INCS + ''');
}

''', '\tunknownOption(opt, val, vlen);\n\treturn 0;\nbad:\n'),
    # helper prints the value form only; incomplete in the caller
    'U6': ('''static int unknownValue(char *opt, char *val, int vlen)
{
	if (!vlen)
		return 0;
	log_printf(1, ''' + UNKS + ''');
	return 1;
}

''', '\tif (!unknownValue(opt, val, vlen))\n\t\t' + INC + '\n\treturn 0;\nbad:\n'),
    # unknown with value as a helper call in the caller's if
    'U7': ('''static void unknownValue(char *opt, char *val)
{
	log_printf(1, ''' + UNKS + ''');
}

''', '\tif (vlen) {\n\t\tunknownValue(opt, val);\n\t\treturn 0;\n\t}\n\t' + INC + '\n\treturn 0;\nbad:\n'),
    'U8': ('''static uint32_t unknownOption(char *opt, char *val, int vlen)
{
	if (vlen)
		log_printf(1, ''' + UNKS + ''');
	else
		log_printf(1, ''' + INCS + ''');
	return 0;
}

''', '\treturn unknownOption(opt, val, vlen);\nbad:\n'),
    'U9': ('''static void unknownOption(char *opt, char *val, size_t vlen)
{
	if (vlen)
		log_printf(1, ''' + UNKS + ''');
	else
		log_printf(1, ''' + INCS + ''');
}

''', '\tunknownOption(opt, val, vlen);\n\treturn 0;\nbad:\n'),
}

KEYS = (('u', "unknown option '"), ('i', 'unknown or incomplete'), ('b', 'parsing option'))


def make(t, s, v):
    assert SB_OLD in t and V_OLD in t and ANCHOR in t
    hs, rs = S[s]
    hv, rv = V[v]
    t = t.replace(SB_OLD, rs, 1).replace(V_OLD, rv, 1)
    if s == 'R1':
        t = t.replace('bad:\n\tlog_printf(1, "\\n\\n***** ERROR: parsing', DONE + 'bad:\n\tlog_printf(1, "\\n\\n***** ERROR: parsing', 1)
    t = t.replace(ANCHOR, hs + hv + ANCHOR, 1)
    return t


def order(text, flags):
    ok, o, d = optlib.compile_src(text, flags, asm=True)
    if not ok:
        return '?'
    s = open(o).read()
    optlib.cleanup(d)
    pos = []
    for k, sub in KEYS:
        m = re.search(r'^LC(\d+):\n\t\.ascii "[^"]*' + re.escape(sub), s, re.M)
        pos.append((int(m.group(1)) if m else -1, k))
    return ''.join(k for _, k in sorted(pos))


FLAGS = optlib.P83


def run(sv):
    s, v = sv
    t = make(optlib.read_src(optlib.SRC), s, v)
    return sv, optlib.score_text(t, FLAGS), order(t, FLAGS)


def main():
    global FLAGS
    a = sys.argv[1:]
    if '-np' in a:
        a.remove('-np')
        FLAGS = []
    if '-p' in a:
        i = a.index('-p')
        FLAGS = ['--param', 'builtin-expect-probability=' + a[i + 1]]
        del a[i:i + 2]
    if a:
        combos = [tuple(x.split(':')) for x in a]
    else:
        combos = [(s, 'E') for s in S] + [('E', v) for v in V if v != 'E']
        if os.environ.get('ALL'):
            combos += [(s, v) for s in S for v in V if s != 'E' and v != 'E']
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, combos))
    for sv, r, o in sorted(res, key=lambda x: x[1].get('total', 99999)):
        print('%-10s %-4s %s' % (':'.join(sv), o, optlib.fmt(r)))
    if os.environ.get('OUT'):
        s, v = combos[-1]
        open(os.environ['OUT'], 'w', newline='\n').write(make(optlib.read_src(optlib.SRC), s, v))


if __name__ == '__main__':
    main()
