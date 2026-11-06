"""Attempt 6: the helpers' "already on" arm as real (live) control flow.

Every caller of optIniBool / optIniBoolG / optN guards it with !(xb.bootFlags & set)
(olddvd's set is 0), so the on arm is dead at every call site, but the functions'
own profiles (estimated before IPA inlining) see it.  Forms for the on arm:
  cp    current: { if (cp) goto r; return 0; }
  ret   if (on) return 0;
  goto  if (on) goto r;        (already on: re-apply, report it on)
  ret1  if (on) return 1;      (already on: report it on, nothing to apply)
and for the off arm: cp (current) or ret.  The `!bad` expect of G/N on/off; optN's entry
test on/off.

python tools/wip/dehint/op6on.py [-fn ib,G,N] [-top N]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = {'ib': '_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)',
       'N': 'static _Bool optN(const char *name, uint32_t set, uint32_t clear, int def)',
       'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)'}
ON = {'cp': '\tif (xb.bootFlags & set) {\n\t\tif (__builtin_constant_p(xb.bootFlags + 1))\n\t\t\tgoto r;\n\t\treturn 0;\n\t}\n',
      'ret': '\tif (xb.bootFlags & set)\n\t\treturn 0;\n',
      'goto': '\tif (xb.bootFlags & set)\n\t\tgoto r;\n',
      'ret1': '\tif (xb.bootFlags & set)\n\t\treturn 1;\n',
      'none': ''}
OFF = {'cp': '\tif (xb.bootFlagsOff & set) {\n\t\tif (__builtin_constant_p(xb.bootFlagsOff + 1))\n\t\t\tgoto r;\n\t\treturn 0;\n\t}\n',
       'ret': '\tif (xb.bootFlagsOff & set)\n\t\treturn 0;\n'}
COST = {'cp': 1, 'ret': 0, 'goto': 0, 'ret1': 0, 'none': 0}


def body(on, off, exp, entry):
    o = '{\n\tchar *bad;\n\n'
    if entry:
        o += '\tif (__builtin_constant_p(xb.bootFlags + 2) == 1) return 0;\n'
    o += ON[on] + OFF[off]
    o += '''	if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\\n", name);
	} else {
		bad = iniBoolInvalid(name);
		if (''' + ('__builtin_expect(!bad, 0)' if exp else '!bad') + ''') {
			if (!getIniBool(name, def))
				return 0;
			log_printf(1, "Using %s option (ini file)\\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad);
			return 0;
		}
	}
r:
	xb.bootFlags &= ~clear;
		xb.bootFlags |= set;
	return 1;
}
'''
    return o


def replace_fn(text, fn, newbody):
    sig = SIG[fn]
    i = text.find(sig)
    j = text.find('\n}\n', i) + 3
    return text[:i] + sig + '\n' + newbody + text[j:]


CUR = {'ib': ('cp', 'cp', False, False), 'G': ('cp', 'cp', True, False), 'N': ('ret', 'cp', True, True)}


def forms(fn):
    exps = (False,) if fn == 'ib' else (False, True)
    ents = (False, True) if fn == 'N' else (False,)
    for on, off, x, e in itertools.product(ON, OFF, exps, ents):
        if on == 'none' and fn != 'N':
            pass
        yield on, off, x, e


def cost(f):
    on, off, x, e = f
    return COST[on] + COST[off] + int(x) + int(e)


def main():
    a = sys.argv[1:]
    fns = ['ib', 'G', 'N']
    top = 40
    if '-fn' in a:
        fns = a[a.index('-fn') + 1].split(',')
    if '-top' in a:
        top = int(a[a.index('-top') + 1])
    base = open(optlib.SRC).read()
    lists = [list(forms(f)) if f in fns else [CUR[f]] for f in ('ib', 'G', 'N')]
    jobs = []
    for combo in itertools.product(*lists):
        t = base
        for fn, f in zip(('ib', 'G', 'N'), combo):
            if f != CUR[fn]:
                t = replace_fn(t, fn, body(*f))
        c = sum(cost(f) for f in combo)
        jobs.append((combo, c, t))
    cur = sum(cost(CUR[f]) for f in CUR)
    print('jobs', len(jobs), 'current cost', cur, flush=True)
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(j[2])), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    for combo, c, r in res[:top]:
        print('%-70s c=%d %s' % (' | '.join('%s/%s%s%s' % (f[0], f[1], '/x' if f[2] else '', '/e' if f[3] else '') for f in combo), c, optlib.fmt(r)))
    print('IDENTICAL cheaper:', [(x[0], x[1]) for x in res if x[2].get('identical') and x[1] < cur])


if __name__ == '__main__':
    main()
