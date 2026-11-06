"""Attempt 7: whole result-variable bodies for optIniBoolG (no builtins at all).

The on/off "already set on the command line" tests set `on = 0` and join the final `on`
test instead of returning (like op7g's on2 lower, whose join DOM/VRP thread away after
inlining).  Tops x lowers x tails.

python tools/wip/dehint/op7w.py [-top N] [-show KEY]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)'
LOG1 = 'log_printf(1, "Using %s option (perbox file)\\n", name);'
LOG2 = 'log_printf(1, "Using %s option (ini file)\\n", name);'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'

# lower: assumes neither flag is set; leaves `on`
LOW = {
    # perbox sets on = 1; ini: on2 style, but no early return
    'L1': f'''if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad)
			on = getIniBool(name, def);
		else {{
			{WARN}
			on = 0;
		}}
		if (on)
			{LOG2}
	}}''',
    # the on2 lower as it is (return 0 inside)
    'L2': f'''if (perboxExists(name)) {{
		{LOG1}
		on = 1;
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
	}}''',
    'L3': f'''if (perboxExists(name)) {{
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
	}}''',
    # the ini log before the warning in source order (optIniBool's .rdata order)
    'L4': f'''if (perboxExists(name)) {{
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
	}}''',
    'L5': f'''if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			if (getIniBool(name, def)) {{
				{LOG2}
				on = 1;
			}} else
				on = 0;
		}} else {{
			{WARN}
			on = 0;
		}}
	}}''',
    'L6': f'''if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		on = 0;
		if (!bad) {{
			if (getIniBool(name, def)) {{
				{LOG2}
				on = 1;
			}}
		}} else
			{WARN}
	}}''',
    'L7': f'''if (perboxExists(name)) {{
		{LOG1}
		on = 1;
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			on = getIniBool(name, def);
			if (!on)
				return 0;
			{LOG2}
		}} else {{
			{WARN}
			on = 0;
		}}
	}}''',
}

TOP = {
    'T1': ('if (xb.bootFlags & set)\n\t\ton = 0;\n\telse if (xb.bootFlagsOff & set)\n\t\ton = 0;\n\telse ', ''),
    'T2': ('if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))\n\t\ton = 0;\n\telse ', ''),
    'T3': ('if (xb.bootFlags & set)\n\t\ton = 0;\n\telse if (xb.bootFlagsOff & set)\n\t\treturn 0;\n\telse ', ''),
    'T4': ('if (xb.bootFlags & set)\n\t\treturn 0;\n\telse if (xb.bootFlagsOff & set)\n\t\ton = 0;\n\telse ', ''),
    'T5': ('on = 0;\n\tif (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) ', ''),
    'T6': ('on = 0;\n\tif (!(xb.bootFlags & set))\n\t\tif (!(xb.bootFlagsOff & set)) ', ''),
}

TAIL = {
    'R1': 'if (!on)\n\t\treturn 0;\n\txb.bootFlags &= ~clear;\n\txb.bootFlags |= set;\n\treturn 1;\n',
    'R2': 'if (on) {\n\t\txb.bootFlags &= ~clear;\n\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n',
    'R3': 'if (on) {\n\t\txb.bootFlags &= ~clear;\n\t\txb.bootFlags |= set;\n\t\treturn 1;\n\t}\n\treturn 0;\n',
}


def body(t, l, r):
    top, _ = TOP[t]
    low = LOW[l]
    if t in ('T5', 'T6'):
        low = '{\n\t' + low.replace('\n', '\n\t') + '\n\t}'
    return '{\n\tchar *bad;\n\t_Bool on;\n\n\t' + top + low + '\n\t' + TAIL[r] + '}\n'


def make(base, key):
    t, l, r = key
    i = base.find(SIG)
    assert i >= 0
    j = base.find('\n}\n', i) + 3
    return base[:i] + SIG + '\n' + body(t, l, r) + base[j:]


def main():
    a = sys.argv[1:]
    top = 30
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = tuple(a[a.index('-show') + 1].split(','))
        out = os.path.join(optlib.BUILD, 'op7w_show.c')
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    jobs = [(k, make(base, k)) for k in itertools.product(TOP, LOW, TAIL)]
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-12s %s' % (' '.join(f), optlib.fmt(r)[:140]))


if __name__ == '__main__':
    main()
