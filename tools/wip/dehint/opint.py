"""Attempt 3: optIniIntI's always_inline.  optIniInt has 3 calls, so gcc 6's early inliner
never takes it (growth * (calls + 1) > early-inlining-insns); the 15% GU profile needs the body
in applyIniOptions before profile_estimate.  So: the int options written out, as a macro or
inline code, in several spellings.

python tools/wip/dehint/opint.py [-o DIR] [names..]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'
II_DEF = '''/* applyIniOptions' copies of the functions above: a function with other
   optimize options can't be inlined into it (always_inline is, early) */
static inline __attribute__((always_inline)) int optIniIntI(const char *name, int def)
{
	char *bad;

	bad = iniU32Invalid(name);
	if (bad) {
		%s
		return def;
	}
	return getIniU32(name, def);
}
''' % WARN
SITE = re.compile(r'\tif \(xb\.(\w+) == -1\)\n\t\txb\.\1 = optIniIntI\("(\w+)", -1\);\n')
CF = '''		xb.cfLdv = optIniIntI("cfldv", 0);
'''


def src():
    t = optlib.read_src(optlib.SRC)
    assert II_DEF in t and CF in t and len(SITE.findall(t)) == 11
    return t


def site_sub(t, fn):
    return SITE.sub(lambda m: fn(m.group(1), m.group(2)), t)


def w(name, field, def_, store_def, neg, ind='\t\t'):
    msg = WARN.replace('name, bad', '"%s", bad' % name)
    if neg:
        s = ind + 'bad = iniU32Invalid("%s");\n' % name
        s += ind + 'if (!bad)\n' + ind + '\txb.%s = getIniU32("%s", %s);\n' % (field, name, def_)
        s += ind + 'else {\n' if store_def else ind + 'else\n'
        s += ind + '\t' + msg + '\n'
        if store_def:
            s += ind + '\txb.%s = %s;\n' % (field, def_) + ind + '}\n'
        return s
    s = ind + 'bad = iniU32Invalid("%s");\n' % name
    s += ind + 'if (bad) {\n' + ind + '\t' + msg + '\n'
    if store_def:
        s += ind + '\txb.%s = %s;\n' % (field, def_)
    s += ind + '} else\n' + ind + '\txb.%s = getIniU32("%s", %s);\n' % (field, name, def_)
    return s


def written(store_def, neg):
    t = src()
    t = site_sub(t, lambda f, n: '\t\tif (xb.%s == -1) {\n' % f + w(n, f, -1, store_def, neg, '\t\t\t') + '\t\t}\n')
    t = t.replace(CF, w('cfldv', 'cfLdv', 0, store_def, neg, '\t\t'))
    t = t.replace('void applyIniOptions(void)\n{\n\tchar *s;\n', 'void applyIniOptions(void)\n{\n\tchar *s, *bad;\n')
    return t.replace(II_DEF, '')


MACRO_SE = '''/* an int option from options.ini, or def if its value is invalid */
#define INI_INT(name, def) ({ \\
	char *bad = iniU32Invalid(name); \\
	int v; \\
	if (bad) { \\
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad); \\
		v = def; \\
	} else \\
		v = getIniU32(name, def); \\
	v; })
'''
MACRO_ST = '''/* an int option from options.ini, unless the value is invalid */
#define INI_INT(var, name, def) do { \\
	char *bad = iniU32Invalid(name); \\
	if (bad) { \\
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad); \\
		var = def; \\
	} else \\
		var = getIniU32(name, def); \\
} while (0)
'''
MACRO_ST2 = MACRO_ST.replace('''		var = def; \\
	} else \\''', '''	} else \\''').replace('if (bad) { \\', 'if (bad) \\').replace('''		log_printf(0,''', '''		log_printf(0,''')
# MACRO_ST2's if/else needs no braces after the replace: fix the shape explicitly
MACRO_ST2 = '''/* an int option from options.ini, unless the value is invalid */
#define INI_INT(var, name, def) do { \\
	char *bad = iniU32Invalid(name); \\
	if (bad) \\
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad); \\
	else \\
		var = getIniU32(name, def); \\
} while (0)
'''


def macro_se():
    t = src().replace(II_DEF, MACRO_SE)
    t = site_sub(t, lambda f, n: '\t\tif (xb.%s == -1)\n\t\t\txb.%s = INI_INT("%s", -1);\n' % (f, f, n))
    return t.replace(CF, '\t\txb.cfLdv = INI_INT("cfldv", 0);\n')


def macro_st(m):
    def f():
        t = src().replace(II_DEF, m)
        t = site_sub(t, lambda f, n: '\t\tif (xb.%s == -1)\n\t\t\tINI_INT(xb.%s, "%s", -1);\n' % (f, f, n))
        return t.replace(CF, '\t\tINI_INT(xb.cfLdv, "cfldv", 0);\n')
    return f


MACRO_TV = '''/* an int option from options.ini, or def if its value is invalid */
#define INI_INT(var, name, def) do { \\
	char *bad = iniU32Invalid(name); \\
	int v; \\
	if (bad) { \\
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad); \\
		v = def; \\
	} else \\
		v = getIniU32(name, def); \\
	var = v; \\
} while (0)
'''


def written_v():
    """written out, with a temporary like the inlined function's return value"""
    def one(name, field, def_, ind):
        msg = WARN.replace('name, bad', '"%s", bad' % name)
        return (ind + 'bad = iniU32Invalid("%s");\n' % name + ind + 'if (bad) {\n' + ind + '\t' + msg + '\n' +
                ind + '\tv = %s;\n' % def_ + ind + '} else\n' + ind + '\tv = getIniU32("%s", %s);\n' % (name, def_) +
                ind + 'xb.%s = v;\n' % field)
    t = src()
    t = site_sub(t, lambda f, n: '\tif (xb.%s == -1) {\n' % f + one(n, f, -1, '\t\t') + '\t}\n')
    t = t.replace(CF, one('cfldv', 'cfLdv', 0, '\t\t'))
    t = t.replace('void applyIniOptions(void)\n{\n\tchar *s;\n\tint i;\n', 'void applyIniOptions(void)\n{\n\tchar *s, *bad;\n\tint i, v;\n')
    return t.replace(II_DEF, '')


V = {
    'm_tv': macro_st(MACRO_TV),
    'w_v': written_v,
    'w_def': lambda: written(True, False),
    'w_nodef': lambda: written(False, False),
    'w_def_neg': lambda: written(True, True),
    'w_nodef_neg': lambda: written(False, True),
    'm_se': macro_se,
    'm_st': macro_st(MACRO_ST),
    'm_st2': macro_st(MACRO_ST2),
}


def run(n):
    return n, optlib.fmt(optlib.score_text(V[n]()))


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if a[:1] == ['-o']:
        out = a[1]
        a = a[2:]
        os.makedirs(out, exist_ok=True)
    names = a or list(V)
    if out:
        for n in names:
            open(os.path.join(out, n + '.c'), 'w', newline='\n').write(V[n]())
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, names):
            print(n, r[:200])
