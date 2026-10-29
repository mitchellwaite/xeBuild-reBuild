"""Coordinate descent over per-option layout hints for applyIniOptions.
python tools/wip/aiosearch.py [tools/wip/aiosearch.json]   -> build/aiosearch/best.{json,c}
Each option is [form, k1, k2, k3]: form 1 = guard + optIniBool call (IPA
inline, callee profile), 0 = the body written out (OPTK, caller context);
k1/k2/k3 = hint on the bootFlags / bootFlagsOff / perboxExists tests
(0 none, 1 expect true, 2 expect false).  Score = tools/wip/blk.py changed lines."""
import json, os, re, subprocess, sys, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.join(ROOT, 'build', 'aiosearch')
os.makedirs(HERE, exist_ok=True)
FL = ['-O3', '--param', 'builtin-expect-probability=83']

MAC = r'''#define EXPK(c, k) ((k) == 1 ? __builtin_expect(!!(c), 1) : (k) == 2 ? __builtin_expect(!!(c), 0) : !!(c))
#define OPTK(name, set, clear, form, k1, k2, k3) \
	if (form) { if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0); } else do { \
		if (EXPK(xb.bootFlags & (set), k1)) \
			break; \
		if (EXPK(xb.bootFlagsOff & (set), k2)) \
			break; \
		if (EXPK(perboxExists(name), k3)) { \
			log_printf(1, "Using %s option (perbox file)\n", name); \
		} else { \
			s = iniBoolInvalid(name); \
			if (!s) { \
				if (!getIniBool(name, 0)) \
					break; \
				log_printf(1, "Using %s option (ini file)\n", name); \
			} else { \
				log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, s); \
				break; \
			} \
		} \
		xb.bootFlags = (xb.bootFlags & ~(clear)) | (set); \
	} while (0)
'''

# optIniBool with the perbox test inverted: in-trace copies then fall
# through to the ini path (noecdremap, as in the original)
FN = r'''_Bool optIniBool(const char *name, u32 set, u32 clear, int def)
{
	char *bad;

	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (!perboxExists(name)) {
		bad = iniBoolInvalid(name);
		if (!bad) {
			if (!getIniBool(name, def))
				return 0;
			log_printf(1, "Using %s option (ini file)\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			return 0;
		}
	} else
		log_printf(1, "Using %s option (perbox file)\n", name);
	{
		/* the original ORs into eax (so `return 1` isn't hoisted) */
		u32 f = (xb.bootFlags & ~clear) | set;
		__asm__("" : "+a" (f));
		xb.bootFlags = f;
	}
	return 1;
}
'''
SRC = open(os.path.join(ROOT, 'tools', 'wip', 'options.c')).read()
SRC = re.sub(r'_Bool optIniBool\(.*?\n}\n', lambda m: FN, SRC, flags=re.S)
I = SRC.index('void applyIniOptions(void)\n{')
HEAD, BODY = SRC[:I], SRC[I:]
BODY = re.sub(r'if \(!\(xb\.bootFlags & (\w+)\)\)\n\t+optIniBool\("(\w+)", \w+, (\w+), 0\);',
              r'OPT("\2", \1, \3);', BODY)
BODY = re.sub(r'optIniBool\("(\w+)", (\w+), (\w+), 0\);', r'OPT("\1", \2, \3);', BODY)
NAMES = re.findall(r'OPT\("(\w+)"', BODY)


def gen(cfg, path):
    body = re.sub(r'OPT\("(\w+)", (\w+), (\w+)\);',
                  lambda m: 'OPTK("%s", %s, %s, %d, %d, %d, %d);' % ((m.group(1), m.group(2), m.group(3)) + tuple(cfg[m.group(1)])),
                  BODY)
    open(path, 'w', newline='\n').write(HEAD + MAC + body)


def score(cfg, path=os.path.join(HERE, 's.c')):
    gen(cfg, path)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'wip', 'blk.py'), path, 'applyIniOptions'] + FL,
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        return 9999
    return sum(1 for l in r.stdout.split('\n') if re.match(r'^[-+][^-+]', l))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cfg = json.load(open(sys.argv[1]))
    else:
        cfg = {n: [0, 1, 2, 1] for n in NAMES}
        cfg['noecdremap'] = [1, 0, 0, 0]
    best = score(cfg)
    print('start', best, flush=True)
    improved = True
    while improved:
        improved = False
        for n in NAMES:
            for v in itertools.product([0, 1], [0, 1, 2], [0, 1, 2], [0, 1, 2]):
                v = list(v)
                if v[0] == 1 and v[1:] != [0, 0, 0]:
                    continue
                if v == cfg[n]:
                    continue
                old = cfg[n]
                cfg[n] = v
                s = score(cfg)
                if s < best:
                    best = s
                    improved = True
                    print(best, n, v, flush=True)
                    json.dump(cfg, open(os.path.join(HERE, 'best.json'), 'w'))
                    gen(cfg, os.path.join(HERE, 'best.c'))
                else:
                    cfg[n] = old
    print('done', best, json.dumps(cfg))
