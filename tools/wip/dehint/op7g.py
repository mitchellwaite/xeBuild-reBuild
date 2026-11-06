"""Attempt 7: natural lower halves (perbox / ini / bad value) for optIniBoolG and optN.

The cp arms (and optN's entry) stay; only the part from `if (perboxExists(name))` to
`return 1;` is replaced, and the `!bad` expect goes.  The idea: a shape whose own
profile_estimate gives the G/N blocks what the expect gives, because its control flow
joins (result variable, shared exits) that DOM/VRP thread away after inlining.

python tools/wip/dehint/op7g.py G|N|GN [-top N] [-show NAME]
"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

LOG1 = 'log_printf(1, "Using %s option (perbox file)\\n", name);'
LOG2 = 'log_printf(1, "Using %s option (ini file)\\n", name);'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'
SET = 'xb.bootFlags &= ~clear;\n\t\txb.bootFlags |= set;'

CUR_G = '''	if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\\n", name);
	} else {
		bad = iniBoolInvalid(name);
		if (__builtin_expect(!bad, 0)) {
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
'''


def lowers():
    L = {}
    L['exp'] = (None, CUR_G)
    L['noexp'] = (None, CUR_G.replace('__builtin_expect(!bad, 0)', '!bad'))
    # result variable, one `if (!on) return 0` for both ini outcomes
    L['on1'] = ('_Bool on;', f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad) {{
			{WARN}
			on = 0;
		}} else
			on = getIniBool(name, def);
		if (!on)
			return 0;
		{LOG2}
	}}
r:
	{SET}
	return 1;
''')
    L['on2'] = ('_Bool on;', f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad)
			on = getIniBool(name, def);
		else {{
			{WARN}
			on = 0;
		}}
		if (!on)
			return 0;
		{LOG2}
	}}
r:
	{SET}
	return 1;
''')
    L['on3'] = ('int on = 0;', f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad)
			{WARN}
		else
			on = getIniBool(name, def);
		if (!on)
			return 0;
		{LOG2}
	}}
r:
	{SET}
	return 1;
''')
    # on covers perbox too
    L['on4'] = ('int on;', f'''	if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad) {{
			{WARN}
			on = 0;
		}} else {{
			on = getIniBool(name, def);
			if (on)
				{LOG2}
		}}
	}}
	if (!on)
		return 0;
r:
	{SET}
	return 1;
''')
    L['on5'] = ('int on;', f'''	if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			on = getIniBool(name, def);
			if (on)
				{LOG2}
		}} else {{
			{WARN}
			on = 0;
		}}
	}}
	if (on) {{
r:
		{SET}
	}}
	return on;
''')
    L['on6'] = ('int on = 0;', f'''	if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad)
			{WARN}
		else if (getIniBool(name, def)) {{
			{LOG2}
			on = 1;
		}}
	}}
	if (on) {{
r:
		{SET}
	}}
	return on;
''')
    # shared 0 exit after the bad warning
    L['out1'] = (None, f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad)
			{WARN}
		else if (getIniBool(name, def)) {{
			{LOG2}
			goto r;
		}}
		return 0;
	}}
r:
	{SET}
	return 1;
''')
    L['out2'] = (None, f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			if (getIniBool(name, def)) {{
				{LOG2}
				goto r;
			}}
		}} else
			{WARN}
		return 0;
	}}
r:
	{SET}
	return 1;
''')
    L['ret1'] = (None, f'''	if (!perboxExists(name)) {{
		bad = iniBoolInvalid(name);
		if (bad) {{
			{WARN}
			return 0;
		}}
		if (!getIniBool(name, def))
			return 0;
		{LOG2}
	}} else
		{LOG1}
r:
	{SET}
	return 1;
''')
    L['inv'] = (None, f'''	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad) {{
			{WARN}
			return 0;
		}} else if (!getIniBool(name, def))
			return 0;
		else
			{LOG2}
	}}
r:
	{SET}
	return 1;
''')
    # result returned at the end
    L['res1'] = ('_Bool on = 0;', f'''	if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad)
			{WARN}
		else if (getIniBool(name, def)) {{
			{LOG2}
			on = 1;
		}}
	}}
	if (on) {{
r:
		{SET}
		return 1;
	}}
	return 0;
''')
    L['res2'] = ('_Bool on = 0;', f'''	if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (bad)
			{WARN}
		else {{
			on = getIniBool(name, def);
			if (on)
				{LOG2}
		}}
	}}
	if (!on)
		return 0;
r:
	{SET}
	return 1;
''')
    return L


SIG = {'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)',
       'N': 'static _Bool optN(const char *name, uint32_t set, uint32_t clear, int def)'}


def make(text, fn, key):
    decl, low = lowers()[key]
    sig = SIG[fn]
    i = text.find(sig)
    j = text.find('\n}\n', i) + 3
    body = text[i:j]
    k = body.find('\tif (perboxExists(name))')
    head = body[:k]
    if decl:
        head = head.replace('\tchar *bad;\n', '\tchar *bad;\n\t' + decl + '\n', 1)
    nb = head + low + '}\n'
    if 'r:' not in nb.split('{', 1)[1].split('if (perboxExists')[0] and 'goto r' not in head:
        pass
    return text[:i] + nb + text[j:]


def main():
    a = sys.argv[1:]
    fns = a.pop(0)
    top = 60
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = a[a.index('-show') + 1]
        t = base
        for f in fns.replace('GN', 'G N').split():
            t = make(t, f, k)
        open(os.path.join(optlib.BUILD, 'op7g_%s_%s.c' % (fns, k)), 'w', newline='\n').write(t)
        print(os.path.join(optlib.BUILD, 'op7g_%s_%s.c' % (fns, k)))
        return
    jobs = []
    keys = list(lowers())
    if fns == 'GN':
        for kg in keys:
            for kn in keys:
                jobs.append(((kg, kn), make(make(base, 'G', kg), 'N', kn)))
    else:
        for k in keys:
            jobs.append(((k,), make(base, fns, k)))
    print('jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-24s %s' % (' '.join(f), optlib.fmt(r)))


if __name__ == '__main__':
    main()
