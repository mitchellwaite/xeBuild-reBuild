"""Attempt 7: optIniBool / optIniBoolG / optN built from parts, on top of op7g's lowers.

Parts: on arm (`cp`: { if (cp) goto r; return 0; }, `ret`: return 0), off arm (same),
entry (`none`, `cp1`: optN's `if (cp(..+2) == 1) return 0;`), lower (op7g.lowers() key).
The other helpers are given by -base: G and N use on2 unless overridden.

python tools/wip/dehint/op7arms.py FN [-top N] [-fix FN=on,off,entry,lower ...] [-lowers k1,k2]
FN: ib | G | N | merge (one helper for G and N) | show:FN=on,off,entry,lower[,FN2=...]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op7g

SIG = {'ib': '_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)',
       'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)',
       'N': 'static _Bool optN(const char *name, uint32_t set, uint32_t clear, int def)'}
CUR = {'ib': ('cp', 'cp', 'none', 'noexp'), 'G': ('cp', 'cp', 'none', 'on2')}
# (before optN was merged into optIniBoolG: 'N': ('ret', 'cp', 'cp1', 'on2'))


def arm(kind, var):
    if kind == 'cp':
        return '\tif (%s & set) {\n\t\tif (__builtin_constant_p(%s + 1))\n\t\t\tgoto r;\n\t\treturn 0;\n\t}\n' % (var, var)
    if kind == 'ret':
        return '\tif (%s & set)\n\t\treturn 0;\n' % var
    if kind == 'r':
        return '\tif (%s & set)\n\t\tgoto r;\n' % var
    if kind == 'r1':
        return '\tif (%s & set)\n\t\treturn 1;\n' % var
    raise ValueError(kind)


def body(on, off, entry, lower):
    decl, low = op7g.lowers()[lower]
    b = '{\n\tchar *bad;\n'
    if decl:
        b += '\t' + decl + '\n'
    b += '\n'
    if entry == 'cp1':
        b += '\tif (__builtin_constant_p(xb.bootFlags + 2) == 1) return 0;\n'
    b += arm(on, 'xb.bootFlags') + arm(off, 'xb.bootFlagsOff') + low + '}\n'
    return b


def put(text, fn, parts):
    sig = SIG[fn]
    i = text.find(sig)
    j = text.find('\n}\n', i) + 3
    return text[:i] + sig + '\n' + body(*parts) + text[j:]


def build(base, cfg):
    t = base
    for fn, parts in cfg.items():
        t = put(t, fn, parts)
    return t


def merge(text, parts):
    """one helper (optIniBoolG) for the G and N sites"""
    t = put(text, 'G', parts)
    i = t.find('/* applyIniOptions\' copy of optIniBool for noecdremap')
    j = t.find('\n}\n', t.find(SIG['N'])) + 3
    t = t[:i] + t[j:].lstrip('\n')
    return t.replace('optN("noecdremap"', 'optIniBoolG("noecdremap"')


def parse(s):
    fn, p = s.split('=')
    return fn, tuple(p.split(','))


def main():
    a = sys.argv[1:]
    mode = a.pop(0)
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    lowk = ['noexp', 'on2', 'on5']
    if '-lowers' in a:
        i = a.index('-lowers'); lowk = a[i + 1].split(','); del a[i:i + 2]
    cfg = dict(CUR)
    while '-fix' in a:
        i = a.index('-fix'); fn, p = parse(a[i + 1]); cfg[fn] = p; del a[i:i + 2]
    base = open(optlib.SRC).read()
    if mode.startswith('show:'):
        for s in mode[5:].split(';'):
            fn, p = parse(s)
            cfg[fn] = p
        t = build(base, cfg)
        out = os.path.join(optlib.BUILD, 'op7arms_show.c')
        open(out, 'w', newline='\n').write(t)
        print(out)
        return
    jobs = []
    arms = ['cp', 'ret']
    if mode == 'merge':
        c = {k: v for k, v in cfg.items() if k != 'N'}
        for on, off, en, lo in itertools.product(arms, arms, ['none', 'cp1'], lowk):
            jobs.append(((on, off, en, lo), merge(build(base, c), (on, off, en, lo))))
    else:
        for on, off, en, lo in itertools.product(arms + (['r', 'r1'] if mode != 'ib' else []), arms,
                                                 ['none', 'cp1'], lowk):
            c = dict(cfg)
            c[mode] = (on, off, en, lo)
            jobs.append(((on, off, en, lo), build(base, c)))
    print('jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-26s %s' % (' '.join(f), optlib.fmt(r)))


if __name__ == '__main__':
    main()
