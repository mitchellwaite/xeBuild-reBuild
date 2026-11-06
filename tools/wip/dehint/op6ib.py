"""Attempt 6: structural (not spelling) shapes of optIniBool / optN / optIniBoolG.

Each helper body is replaced by a whole natural shape (Linux v1.16's single
`a || b` exit, nested ifs, an `out:` exit, a result variable, an `ok` flag, ...)
with every builtin of that helper gone, optionally keeping the `!bad` expect (G, N) or
optN's entry test.  Other helpers are left as in src.

python tools/wip/dehint/op6ib.py FN [-top N]     FN: ib | N | G | all (one shape for all three)
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = {'ib': '_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)',
       'N': 'static _Bool optN(const char *name, uint32_t set, uint32_t clear, int def)',
       'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)'}

LOG1 = 'log_printf(1, "Using %s option (perbox file)\\n", name);'
LOG2 = 'log_printf(1, "Using %s option (ini file)\\n", name);'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'
SET = 'xb.bootFlags &= ~clear;\n\txb.bootFlags |= set;'
ENTRY = '\tif (__builtin_constant_p(xb.bootFlags + 2) == 1) return 0;\n'


def nb(exp):
    return '__builtin_expect(!bad, 0)' if exp else '!bad'


def shapes(exp):
    B = nb(exp)
    S = {}
    # Linux v1.16: one exit for both flags
    S['or'] = f'''	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if ({B}) {{
			if (!getIniBool(name, def))
				return 0;
			{LOG2}
		}} else {{
			{WARN}
			return 0;
		}}
	}}
	{SET}
	return 1;
'''
    S['plain'] = S['or'].replace('\tif ((xb.bootFlags & set) || (xb.bootFlagsOff & set))\n\t\treturn 0;',
                                 '\tif (xb.bootFlags & set)\n\t\treturn 0;\n\tif (xb.bootFlagsOff & set)\n\t\treturn 0;')
    S['bitor'] = S['or'].replace('(xb.bootFlags & set) || (xb.bootFlagsOff & set)',
                                 '(xb.bootFlags | xb.bootFlagsOff) & set')
    S['and'] = f'''	if (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) {{
		if (perboxExists(name)) {{
			{LOG1}
		}} else {{
			bad = iniBoolInvalid(name);
			if ({B}) {{
				if (!getIniBool(name, def))
					return 0;
				{LOG2}
			}} else {{
				{WARN}
				return 0;
			}}
		}}
		{SET}
		return 1;
	}}
	return 0;
'''
    S['nest'] = f'''	if (!(xb.bootFlags & set)) {{
		if (!(xb.bootFlagsOff & set)) {{
			if (perboxExists(name)) {{
				{LOG1}
			}} else {{
				bad = iniBoolInvalid(name);
				if ({B}) {{
					if (!getIniBool(name, def))
						return 0;
					{LOG2}
				}} else {{
					{WARN}
					return 0;
				}}
			}}
			{SET}
			return 1;
		}}
	}}
	return 0;
'''
    S['out'] = f'''	if (xb.bootFlags & set)
		goto out;
	if (xb.bootFlagsOff & set)
		goto out;
	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if ({B}) {{
			if (!getIniBool(name, def))
				goto out;
			{LOG2}
		}} else {{
			{WARN}
			goto out;
		}}
	}}
	{SET}
	return 1;
out:
	return 0;
'''
    S['rvar'] = f'''	_Bool r = 0;

	if (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) {{
		if (perboxExists(name)) {{
			{LOG1}
			r = 1;
		}} else {{
			bad = iniBoolInvalid(name);
			if ({B}) {{
				if (getIniBool(name, def)) {{
					{LOG2}
					r = 1;
				}}
			}} else
				{WARN}
		}}
		if (r) {{
			{SET}
		}}
	}}
	return r;
'''
    S['ok'] = f'''	_Bool ok;

	if (xb.bootFlags & set)
		return 0;
	if (xb.bootFlagsOff & set)
		return 0;
	if (perboxExists(name)) {{
		{LOG1}
		ok = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if ({B}) {{
			ok = getIniBool(name, def);
			if (ok)
				{LOG2}
		}} else {{
			{WARN}
			ok = 0;
		}}
	}}
	if (ok) {{
		{SET}
	}}
	return ok;
'''
    S['okor'] = S['ok'].replace('\tif (xb.bootFlags & set)\n\t\treturn 0;\n\tif (xb.bootFlagsOff & set)\n\t\treturn 0;',
                                '\tif ((xb.bootFlags & set) || (xb.bootFlagsOff & set))\n\t\treturn 0;')
    S['badfirst'] = f'''	if (xb.bootFlags & set)
		return 0;
	if (xb.bootFlagsOff & set)
		return 0;
	if (perboxExists(name))
		{LOG1}
	else {{
		bad = iniBoolInvalid(name);
		if ({'__builtin_expect(bad != 0, 1)' if exp else 'bad'}) {{
			{WARN}
			return 0;
		}}
		if (!getIniBool(name, def))
			return 0;
		{LOG2}
	}}
	{SET}
	return 1;
'''
    S['elseif'] = f'''	if (xb.bootFlags & set)
		return 0;
	if (xb.bootFlagsOff & set)
		return 0;
	if (perboxExists(name))
		{LOG1}
	else if ((bad = iniBoolInvalid(name))) {{
		{WARN}
		return 0;
	}} else if (getIniBool(name, def))
		{LOG2}
	else
		return 0;
	{SET}
	return 1;
'''
    S['perbox_ret'] = f'''	if (xb.bootFlags & set)
		return 0;
	if (xb.bootFlagsOff & set)
		return 0;
	if (perboxExists(name)) {{
		{LOG1}
		{SET}
		return 1;
	}}
	bad = iniBoolInvalid(name);
	if ({B}) {{
		if (getIniBool(name, def)) {{
			{LOG2}
			{SET}
			return 1;
		}}
		return 0;
	}}
	{WARN}
	return 0;
'''
    return S


def make(fn, shape, exp, entry):
    b = shapes(exp)[shape]
    head = '{\n\tchar *bad;\n'
    if shape in ('rvar', 'ok', 'okor'):
        decl, rest = b.split('\n', 1)
        head += decl + '\n'
        b = rest
    head += '\n'
    if entry:
        head += ENTRY
    return head + b + '}\n'


def replace_fn(text, fn, newbody):
    sig = SIG[fn]
    i = text.find(sig)
    assert i >= 0, fn
    j = text.find('\n}\n', i) + 3
    return text[:i] + sig + '\n' + newbody + text[j:]


def main():
    a = sys.argv[1:]
    fn = a.pop(0)
    top = 60
    if '-top' in a:
        i = a.index('-top')
        top = int(a[i + 1])
    base = open(optlib.SRC).read()
    jobs = []
    names = list(shapes(False))
    if fn == 'all':
        for s in names:
            for xg in (False, True):
                for xn in (False, True):
                    for en in (False, True):
                        t = replace_fn(base, 'ib', make('ib', s, False, False))
                        t = replace_fn(t, 'G', make('G', s, xg, False))
                        t = replace_fn(t, 'N', make('N', s, xn, en))
                        jobs.append(((s, 'Gexp' if xg else '', 'Nexp' if xn else '', 'Nent' if en else ''), t))
    else:
        for s in names:
            for x in ((False, True) if fn != 'ib' else (False,)):
                for en in ((False, True) if fn == 'N' else (False,)):
                    jobs.append(((s, 'exp' if x else '', 'ent' if en else ''),
                                 replace_fn(base, fn, make(fn, s, x, en))))
    print('jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-40s %s' % (' '.join(x for x in f if x), optlib.fmt(r)))


if __name__ == '__main__':
    main()
