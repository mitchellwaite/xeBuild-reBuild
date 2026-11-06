"""Attempt 3: optIniBoolG / optN sites as code in applyIniOptions (a statement-expression macro
of optIniBool's body, so it is there before profile_estimate, like INI_INT), instead of the
IPA-inlined hinted copies.

python tools/wip/dehint/opgm.py"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

INI = 'log_printf(1, "Using %s option (ini file)\\\\n", name); \\'
PER = 'log_printf(1, "Using %s option (perbox file)\\\\n", name); \\'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\\\n", name, bad); \\'


def macro(cp, exp):
    a1 = ('if (xb.bootFlags & set) { if (__builtin_constant_p(xb.bootFlags + 1)) goto r; r_ = 0; goto e; } \\'
          if cp else 'if (xb.bootFlags & set) { r_ = 0; goto e; } \\')
    a2 = ('if (xb.bootFlagsOff & set) { if (__builtin_constant_p(xb.bootFlagsOff + 1)) goto r; r_ = 0; goto e; } \\'
          if cp else 'if (xb.bootFlagsOff & set) { r_ = 0; goto e; } \\')
    t = '!bad' if not exp else '__builtin_expect(!bad, 0)'
    return '''#define OPTB(name, set, clear, def) ({ \\
	__label__ r, e; \\
	char *bad; \\
	_Bool r_ = 1; \\
	%s
	%s
	if (perboxExists(name)) { \\
		%s
	} else { \\
		bad = iniBoolInvalid(name); \\
		if (%s) { \\
			if (!getIniBool(name, def)) { r_ = 0; goto e; } \\
			%s
		} else { \\
			%s
			r_ = 0; goto e; \\
		} \\
	} \\
r: \\
	xb.bootFlags &= ~(clear); \\
	xb.bootFlags |= (set); \\
e: \\
	r_; })

''' % (a1, a2, PER, t, INI, WARN)


SITES_G = ['if (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);',
           'if (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);',
           'if (!(xb.bootFlags & (1))) optIniBoolG("cygnos", 1, 0, 0);',
           'if (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);']
SITE_N = 'if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);'


def build(sites, cp, exp):
    t = optlib.read_src(optlib.SRC)
    k = t.index('/* options from perbox files and options.ini')
    t = t[:k] + macro(cp, exp) + t[k:]
    for s in sites:
        assert s in t, s
        t = t.replace(s, s.replace('optIniBoolG(', 'OPTB(').replace('optN(', 'OPTB('))
    return t


V = {}
for cp in (0, 1):
    for exp in (0, 1):
        V['G_cp%d_e%d' % (cp, exp)] = (SITES_G, cp, exp)
        V['N_cp%d_e%d' % (cp, exp)] = ([SITE_N], cp, exp)
        V['GN_cp%d_e%d' % (cp, exp)] = (SITES_G + [SITE_N], cp, exp)

if __name__ == '__main__':
    names = sys.argv[1:] or list(V)
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(lambda n: (n, optlib.fmt(optlib.score_text(build(*V[n])))), names):
            print(n, r[:160])
