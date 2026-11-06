"""Attempt 6: the optIniBoolG / optN sites written out in applyIniOptions as plain nested
ifs (the way Linux v1.16's inlined code reads), with no helper, no returns and no builtins,
so their profile is estimated in applyIniOptions itself.

python tools/wip/dehint/op6w.py [shape ...]
Sites: G (nandmu, nosecurity, cygnos, smcnoeject), N (noecdremap), GN, and each single site.
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SITES = {
    'nandmu': ('if (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);', 'nandmu', '0x10000000'),
    'nosecurity': ('if (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);', 'nosecurity', '0x4000000'),
    'cygnos': ('if (!(xb.bootFlags & (1))) optIniBoolG("cygnos", 1, 0, 0);', 'cygnos', '1'),
    'smcnoeject': ('if (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);', 'smcnoeject', '0x400000'),
    'noecdremap': ('if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);', 'noecdremap', '0x80000000'),
}
L1 = 'log_printf(1, "Using %s option (perbox file)\\n", "{n}");'
L2 = 'log_printf(1, "Using %s option (ini file)\\n", "{n}");'
W = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", "{n}", s);'


def shape(k, n, b):
    l1, l2, w = L1.format(n=n), L2.format(n=n), W.format(n=n)
    G = {'and': f'!(xb.bootFlags & {b}) && !(xb.bootFlagsOff & {b})'}
    S = {}
    S['w1'] = f'''if ({G['and']}) {{
		if (perboxExists("{n}")) {{
			{l1}
			xb.bootFlags |= {b};
		}} else {{
			s = iniBoolInvalid("{n}");
			if (!s) {{
				if (getIniBool("{n}", 0)) {{
					{l2}
					xb.bootFlags |= {b};
				}}
			}} else
				{w}
		}}
	}}'''
    S['w2'] = f'''if ({G['and']}) {{
		if (perboxExists("{n}")) {{
			{l1}
			xb.bootFlags |= {b};
		}} else {{
			s = iniBoolInvalid("{n}");
			if (s)
				{w}
			else if (getIniBool("{n}", 0)) {{
				{l2}
				xb.bootFlags |= {b};
			}}
		}}
	}}'''
    S['w3'] = f'''if ({G['and']}) {{
		i = 0;
		if (perboxExists("{n}")) {{
			{l1}
			i = 1;
		}} else {{
			s = iniBoolInvalid("{n}");
			if (!s) {{
				if (getIniBool("{n}", 0)) {{
					{l2}
					i = 1;
				}}
			}} else
				{w}
		}}
		if (i)
			xb.bootFlags |= {b};
	}}'''
    S['w4'] = S['w1'].replace(G['and'] + ') {', f'!(xb.bootFlags & {b})) {{ if (!(xb.bootFlagsOff & {b})) {{', 1) + ' }'
    S['w5'] = f'''if ({G['and']}) {{
		if (perboxExists("{n}"))
			{l1}
		else {{
			s = iniBoolInvalid("{n}");
			if (s) {{
				{w}
				goto n_{n};
			}}
			if (!getIniBool("{n}", 0))
				goto n_{n};
			{l2}
		}}
		xb.bootFlags |= {b};
	}}
n_{n}:'''
    S['w6'] = f'''if ({G['and']}) {{
		if (perboxExists("{n}")) {{
			{l1}
			xb.bootFlags |= {b};
		}} else if ((s = iniBoolInvalid("{n}"))) {{
			{w}
		}} else if (getIniBool("{n}", 0)) {{
			{l2}
			xb.bootFlags |= {b};
		}}
	}}'''
    return S[k]


GROUPS = {'G': ['nandmu', 'nosecurity', 'cygnos', 'smcnoeject'], 'N': ['noecdremap'],
          'GN': ['nandmu', 'nosecurity', 'cygnos', 'smcnoeject', 'noecdremap']}
for s in SITES:
    GROUPS[s] = [s]


def build(k, group):
    t = optlib.read_src(optlib.SRC)
    for s in GROUPS[group]:
        old, n, b = SITES[s]
        assert old in t, old
        t = t.replace(old, shape(k, n, b))
    return t


if __name__ == '__main__':
    shapes = sys.argv[1:] or ['w1', 'w2', 'w3', 'w4', 'w5', 'w6']
    jobs = [(k, g) for k in shapes for g in GROUPS]
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as ex:
        res = list(ex.map(lambda j: (j, optlib.score_text(build(*j))), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for j, r in res:
        print('%-4s %-12s %s' % (j[0], j[1], optlib.fmt(r)[:150]))
