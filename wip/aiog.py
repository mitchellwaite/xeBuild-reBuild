"""applyIniOptions without a profile: variants of src/options.c for gcc's
guessed profile.

python wip/aiog.py <cfg.json> <out.c>

Drops the profile build's pieces (the no-branch-probabilities pragmas, the
aio_never dead edges of the crafted design) and writes each bool option as
OPTK(name, set, clear, form, k1, k2, k3): form 1 = guard + optIniBool call
(IPA-inlined, callee profile), 0 = the body in the caller; k1/k2/k3 = hint
on the bootFlags / bootFlagsOff / perboxExists tests (0 none, 1 expect true,
2 expect false).  cfg: {"opts": {name: [form, k1, k2, k3]}} or the plain
{name: [...]} of wip/aiosearch.json; `-` = no hints, all form 0.
"""
import json, re, sys

ROOT = __file__.replace('\\', '/').rsplit('/wip/', 1)[0]
MAC = r'''#define EXPK(c, k) ((k) == 1 ? __builtin_expect(!!(c), 1) : (k) == 2 ? __builtin_expect(!!(c), 0) : !!(c))
#define OPTK(name, set, clear, form, k1, k2, k3) \
	if (form) { if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0); } else do { \
		if (EXPK(xb.bootFlags & (set), k1)) \
			break; \
		if (EXPK(xb.bootFlagsOff & (set), k2)) \
			break; \
		if (EXPK(perboxExists(name), k3)) { \
			log_printf(1, msg_optPerbox, name); \
		} else { \
			s = iniBoolInvalid(name); \
			if (!s) { \
				if (!getIniBool(name, 0)) \
					break; \
				log_printf(1, msg_optIni, name); \
			} else { \
				log_printf(0, msg_iniInvalid, name, s); \
				break; \
			} \
		} \
		xb.bootFlags &= ~(clear); \
		xb.bootFlags |= (set); \
	} while (0)
'''


def cut(t, a, b):
    i = t.index(a)
    j = t.index(b, i) + len(b)
    return t[:i], t[j:]


def gen(cfg, src=None):
    t = src or open(ROOT + '/src/options.c').read()
    for l in ['#pragma GCC push_options\n', '#pragma GCC pop_options\n',
              '#pragma GCC optimize ("no-branch-probabilities", "no-reorder-functions")\n']:
        t = t.replace(l, '')
    t = t.replace('parseButtonI(getIniValue(str_xellbutton2), aio_never)',
                  'parseButtonI(getIniValue(str_xellbutton2), 0)')
    h, r = cut(t, '\t\t/* OPT(str_olddvd, 0, 4) with dead edges', '\t\t} while (0);\n')
    t = h + '\t\tOPT(str_olddvd, 0, 4);\n' + r
    h, r = cut(t, '\t} else if (aio_never) {', '\t\tgoto tail;\n\t}\n')
    t = h + '\t}\n' + r
    t = t.replace('blsuffix:\n', '')
    h, r = cut(t, '\t/* a dead cycle through the blSuffix test', '\t\tgoto blsuffix;\n')
    t = h + r
    a = t.index('void applyIniOptions(void)')
    body = t[a:t.index('\n}\n', a)]
    assert 'aio_never' not in body and 'goto' not in body, 'leftover dead edges'
    t = t.replace('#define OPT(name, set, clear) do {', MAC + '#define OPT_UNUSED(name, set, clear) do {')
    opts = cfg.get('opts', cfg)     # (or a plain wip/aiosearch.json)

    def rep(m):
        n = m.group(1)
        v = opts.get(n, [0, 0, 0, 0])
        return 'OPTK(str_%s, %s, %s, %d, %d, %d, %d);' % ((n, m.group(2), m.group(3)) + tuple(v))
    i = t.index('void applyIniOptions(void)')
    t = t[:i] + re.sub(r'OPT\(str_(\w+), (\w+), (\w+)\);', rep, t[i:])
    return t


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1])) if sys.argv[1] != '-' else {}
    open(sys.argv[2], 'w', newline='\n').write(gen(cfg))
