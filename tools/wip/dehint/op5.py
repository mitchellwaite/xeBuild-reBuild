"""Attempt 5: control flow inside the dead arms of optIniBool / optN / optIniBoolG.

Each helper is regenerated from a template: the on/off arms are either plain
(`if (x & set) return 0;`) or `{ if (cp) <stmt>; return 0; }` with <stmt> a goto to a
label anywhere in the body, or a return; optN's entry test likewise; the `!bad` expect on
or off.  Other tricks may be removed too (optricks names, -r a,b).

python tools/wip/dehint/op5.py FN [-r removals] [-only-fewer] [-top N]
  FN: ib | N | G
Prints the best forms; `fewer` marks forms with fewer builtins than the current source."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

HDR = {'ib': '_Bool optIniBool(', 'N': 'static _Bool optN(', 'G': 'static _Bool optIniBoolG('}
SIG = {'ib': '_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)',
       'N': 'static _Bool optN(const char *name, uint32_t set, uint32_t clear, int def)',
       'G': 'static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)'}

LABELS = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'r', 'L8']
# statements a dead arm can run
STMTS = ['goto %s;' % l for l in LABELS] + ['return 1;']


def body(entry, on, off, exp, onret='return 0;', offret='return 0;'):
    """entry/on/off: None (plain, or no entry test) or a statement; entry 'keep' = current"""
    oncmp = offcmp = ''
    if on and '|' in on:
        oncmp, on = on.split('|')
    if off and '|' in off:
        offcmp, off = off.split('|')
    used = set()
    for s in (entry, on, off):
        if s and s.startswith('goto '):
            used.add(s[5:-1])

    def lab(l):
        return (l + ':\n') if l in used else ''
    o = ['{', '\tchar *bad;', '']
    if entry == 'keep':
        o.append('\tif (__builtin_constant_p(xb.bootFlags + 2) == 1) return 0;')
    elif entry:
        o.append('\tif (__builtin_constant_p(xb.bootFlags + 2) == 1) %s' % entry)
    if on:
        o.append('\tif (xb.bootFlags & set) {\n\t\tif (__builtin_constant_p(xb.bootFlags + 1)%s)\n\t\t\t%s\n\t\t%s\n\t}' % (oncmp, on, onret))
    else:
        o.append('\tif (xb.bootFlags & set)\n\t\treturn 0;')
    o.append(lab('L0').rstrip('\n')) if 'L0' in used else None
    if off:
        o.append('\tif (xb.bootFlagsOff & set) {\n\t\tif (__builtin_constant_p(xb.bootFlagsOff + 1)%s)\n\t\t\t%s\n\t\t%s\n\t}' % (offcmp, off, offret))
    else:
        o.append('\tif (xb.bootFlagsOff & set)\n\t\treturn 0;')
    if 'L1' in used:
        o.append('L1:')
    o.append('\tif (perboxExists(name)) {')
    if 'L2' in used:
        o.append('L2:')
    o.append('\t\tlog_printf(1, "Using %s option (perbox file)\\n", name);')
    o.append('\t} else {')
    if 'L3' in used:
        o.append('L3:')
    o.append('\t\tbad = iniBoolInvalid(name);')
    o.append('\t\tif (__builtin_expect(!bad, 0)) {' if exp else '\t\tif (!bad) {')
    if 'L4' in used:
        o.append('L4:')
    o.append('\t\t\tif (!getIniBool(name, def))\n\t\t\t\treturn 0;')
    if 'L5' in used:
        o.append('L5:')
    o.append('\t\t\tlog_printf(1, "Using %s option (ini file)\\n", name);')
    o.append('\t\t} else {')
    if 'L6' in used:
        o.append('L6:')
    o.append('\t\t\tlog_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);')
    o.append('\t\t\treturn 0;')
    o.append('\t\t}')
    o.append('\t}')
    o.append('r:')
    o.append('\txb.bootFlags &= ~clear;')
    o.append('\t\txb.bootFlags |= set;')
    if 'L8' in used:
        o.append('L8:')
    o.append('\treturn 1;')
    o.append('}')
    return '\n'.join(o) + '\n'


def replace_fn(text, fn, newbody):
    sig = SIG[fn]
    i = text.find(sig)
    assert i >= 0, fn
    j = text.find('\n}\n', i) + 3
    return text[:i] + sig + '\n' + newbody + text[j:]


CUR = {'ib': (None, 'goto r;', 'goto r;', False),
       'N': ('keep', None, 'goto r;', True),
       'G': (None, 'goto r;', 'goto r;', True)}


def ntricks(fn, entry, on, off, exp):
    return (1 if entry else 0) + (1 if on else 0) + (1 if off else 0) + (1 if exp else 0)


def forms(fn):
    arms = [None] + STMTS
    onarms = arms
    offarms = [a for a in arms if a != 'goto L0;']
    entries = [None]
    if fn == 'N':
        entries = [None, 'keep'] + [s for s in STMTS]
    exps = [False, True] if fn != 'ib' else [False]
    for e, a, b, x in itertools.product(entries, onarms, offarms, exps):
        if b == 'goto L0;':
            continue
        yield e, a, b, x


def main():
    a = sys.argv[1:]
    fn = a.pop(0)
    rem = []
    if '-r' in a:
        i = a.index('-r')
        rem = [x for x in a[i + 1].split(',') if x]
        del a[i:i + 2]
    top = 40
    if '-top' in a:
        i = a.index('-top')
        top = int(a[i + 1])
        del a[i:i + 2]
    onlyfewer = '-only-fewer' in a
    base, got = optricks.apply(optricks.base(), rem)
    cur_n = ntricks(fn, *CUR[fn])
    jobs = []
    for f in forms(fn):
        n = ntricks(fn, *f)
        if onlyfewer and n >= cur_n:
            continue
        jobs.append((f, n, replace_fn(base, fn, body(*f))))
    print('removals', got, 'jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4))) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(j[2], optricks.flags_for(rem))), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    for f, n, r in res[:top]:
        print('%-60s n=%d%s %s' % (repr(f), n, ' FEWER' if n < cur_n else '', optlib.fmt(r)))
    idn = [x for x in res if x[2].get('identical') and x[1] < cur_n]
    print('IDENTICAL with fewer:', [(x[0], x[1]) for x in idn])


if __name__ == '__main__':
    main()
