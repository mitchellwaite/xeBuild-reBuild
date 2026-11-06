"""Attempt 7: optIniBool (ib) as a result-variable function, with returns mixed in.

op7pe showed what the OPT sites' profile needs from ib (the cp-arm source): `!bad` 21.6%
(pointer 15 & early return 61: the warning arm returns), the getIniBool test 61/39 (early
return on !getIniBool), r ~6002.  Parts:
  top   T0 both flag tests return 0, T1 both set on = 0, T2 `||` sets on = 0, T3 on arm on = 0 /
        off returns, T4 on returns / off on = 0, T5 `on = 0; if (!a && !b) {...}`
  ini   a `on = getIniBool(); if (on) log`, b `on = getIniBool(); if (!on) return 0; log`,
        c `if (getIniBool()) { log; on = 1; } else on = 0;`, d `if (!getIniBool()) return 0;
        log; on = 1;`
  warn  ret (return 0) | on0 (on = 0)
  tail  R1 `if (!on) return 0; set; return 1`, R2 `if (on) set; return on`
python tools/wip/dehint/op7ib.py [-fn ib|G] [-top N] [-show top,ini,warn,tail]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = {'ib': '_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)',
       'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)'}
LOG1 = 'log_printf(1, "Using %s option (perbox file)\\n", name);'
LOG2 = 'log_printf(1, "Using %s option (ini file)\\n", name);'
WARN = 'log_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);'

INI = {
    'a': 'on = getIniBool(name, def);\n\t\t\tif (on)\n\t\t\t\t' + LOG2,
    'b': 'on = getIniBool(name, def);\n\t\t\tif (!on)\n\t\t\t\treturn 0;\n\t\t\t' + LOG2,
    'c': 'if (getIniBool(name, def)) {\n\t\t\t\t' + LOG2 + '\n\t\t\t\ton = 1;\n\t\t\t} else\n\t\t\t\ton = 0;',
    'd': 'if (!getIniBool(name, def))\n\t\t\t\treturn 0;\n\t\t\t' + LOG2 + '\n\t\t\ton = 1;',
}
WARNS = {'ret': WARN + '\n\t\t\treturn 0;', 'on0': WARN + '\n\t\t\ton = 0;'}


def lower(ini, warn):
    return (f'if (perboxExists(name)) {{\n\t\t{LOG1}\n\t\ton = 1;\n\t}} else {{\n'
            f'\t\tbad = iniBoolInvalid(name);\n\t\tif (!bad) {{\n\t\t\t{INI[ini]}\n\t\t}} else {{\n'
            f'\t\t\t{WARNS[warn]}\n\t\t}}\n\t}}')


TOP = {
    'T0': 'if (xb.bootFlags & set)\n\t\treturn 0;\n\tif (xb.bootFlagsOff & set)\n\t\treturn 0;\n\t',
    'T1': 'if (xb.bootFlags & set)\n\t\ton = 0;\n\telse if (xb.bootFlagsOff & set)\n\t\ton = 0;\n\telse ',
    'T2': 'if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))\n\t\ton = 0;\n\telse ',
    'T3': 'if (xb.bootFlags & set)\n\t\ton = 0;\n\telse if (xb.bootFlagsOff & set)\n\t\treturn 0;\n\telse ',
    'T4': 'if (xb.bootFlags & set)\n\t\treturn 0;\n\telse if (xb.bootFlagsOff & set)\n\t\ton = 0;\n\telse ',
    'T5': 'on = 0;\n\tif (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) ',
}
TAIL = {
    'R1': 'if (!on)\n\t\treturn 0;\n\txb.bootFlags &= ~clear;\n\txb.bootFlags |= set;\n\treturn 1;\n',
    'R2': 'if (on) {\n\t\txb.bootFlags &= ~clear;\n\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n',
}


def body(t, ini, warn, r):
    low = lower(ini, warn)
    if t == 'T5':
        low = '{\n\t' + low.replace('\n', '\n\t') + '\n\t}'
    return '{\n\tchar *bad;\n\t_Bool on;\n\n\t' + TOP[t] + low + '\n\t' + TAIL[r] + '}\n'


def make(base, fn, key):
    sig = SIG[fn]
    i = base.find(sig)
    assert i >= 0
    j = base.find('\n}\n', i) + 3
    return base[:i] + sig + '\n' + body(*key) + base[j:]


def main():
    a = sys.argv[1:]
    top = 30
    fn = 'ib'
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    if '-fn' in a:
        i = a.index('-fn'); fn = a[i + 1]; del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = tuple(a[a.index('-show') + 1].split(','))
        out = os.path.join(optlib.BUILD, 'op7ib_show.c')
        open(out, 'w', newline='\n').write(make(base, fn, k))
        print(out)
        return
    jobs = [(k, make(base, fn, k)) for k in itertools.product(TOP, INI, WARNS, TAIL)]
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-16s %s' % (' '.join(f), optlib.fmt(r)[:140]))


if __name__ == '__main__':
    main()
