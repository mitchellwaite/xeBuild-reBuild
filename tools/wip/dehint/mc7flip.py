"""mode_client attempt 7: the loop latch compare flip (`cmp esi,eax; jle` vs `cmp eax,esi;
jge`, PRE's latch phi takes a recycled SSA name: prephitmp_580 fresh in the reference
state, prephitmp_4 recycled after a feed removal) shows up in several near misses.  Try
count-neutral respellings of the inlined helpers' bodies (oneArg from mc6v_one, wbArgs,
bpArgs) and mc5nat's rules on near-miss bases.

python tools/wip/dehint/mc7flip.py BASE.c [BASE2.c ...] [-j 4]"""
import os, runpy, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc5nat

HERE = os.path.dirname(os.path.abspath(__file__))
ONE = runpy.run_path(os.path.join(HERE, 'mc6v_one.py'))

WB_OLD = '''	j++;
	b = argv[j];
	if (!b || j == argc || *b == '-')
		client_usage(4, argv[i]);
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	*pi = j;
	return argv[i + 1];
}'''
WB = {
    'wb_j2': WB_OLD.replace('\tj++;\n\tb = argv[j];', '\tj = i + 2;\n\tb = argv[j];'),
    'wb_bj': WB_OLD.replace('\tj++;\n\tb = argv[j];', '\tb = argv[++j];'),
    'wb_reta': WB_OLD.replace('return argv[i + 1];', 'return a;'),
    'wb_pi': WB_OLD.replace('\t*pi = j;\n\treturn argv[i + 1];', '\t*pi = i + 2;\n\treturn argv[i + 1];'),
}
BP_OLD = '''	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	*pi = j;
	return argv[i + 1];
}

/* -wb'''
BP = {
    'bp_reta': BP_OLD.replace('return argv[i + 1];', 'return a;'),
    'bp_pi2': BP_OLD.replace('*pi = j;', '*pi = i + 2;'),
}


def variants(t):
    out = []
    for k, subs in ONE['V'].items():
        if not k.startswith('n_'):
            continue
        old, new = subs[0]
        if t.count(old) == 1:
            out.append((k, t.replace(old, new)))
    for k, new in WB.items():
        if t.count(WB_OLD) == 1:
            out.append((k, t.replace(WB_OLD, new)))
    for k, new in BP.items():
        if t.count(BP_OLD) == 1:
            out.append((k, t.replace(BP_OLD, new)))
    out += mc5nat.variants(t, None)
    return out


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    bases = [x for x in a if x.endswith('.c')]
    for b in bases:
        t = mc1lib.read_src(b)
        vs = variants(t)
        print(b, mc1.count(t)['total'], mc1lib.fmt(mc1lib.score_text(t))[:40], len(vs), 'variants', flush=True)
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda kv: (kv[0], mc1lib.score_text(kv[1]), kv[1]), vs))
        rows = []
        for k, s, txt in res:
            if 'compile' in s:
                continue
            d = 0 if s['identical'] else s['total']
            if d == 0:
                print('HIT', b, k, 'count', mc1.count(txt)['total'], flush=True)
            rows.append((d, k))
        rows.sort()
        print('  best', rows[:10], flush=True)


if __name__ == '__main__':
    main()
