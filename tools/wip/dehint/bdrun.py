"""python tools/wip/dehint/bdrun.py <gen.py> [-n TOP] [-f fn,fn] [-k label]: score whole-source variants, strict and loose together.

A generator defines CASES(base) -> [(label, text or fn(text)->text)], optional BASE (file relative to the repo, default src/build.c).
Sorted by loose then strict lines, over FOCUS functions when -f or the generator's FOCUS gives them.  Writes the best (or -k label's) to
build/bd/<gen>_best.c.  Also a helper module: fnspan and sub for generators."""
import difflib, importlib.util, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib


def loose(ls):
    ls = [re.sub(r'^(j\w+|call)\s+[0-9a-f]+$', r'\1', l) for l in ls]
    return [l for l in ls if not re.match(r'^(nop|xchg\s+ax,ax|lea\s+(esi|edi),\[(esi|edi).*\]|mov\s+esi,esi)', l)]


def ndiff(a, b):
    if a == b:
        return 0
    n = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal':
            n += (i2 - i1) + (j2 - j1)
    return n


def score(text, flags=None):
    ok, o, d = bdlib.compile_src(text, bdlib.P98 if flags is None else flags)
    try:
        if not ok:
            return {'err': o[:300]}
        r = bdlib.ref()
        if open(o, 'rb').read() == r['bytes']:
            return {'identical': True, 'S': {}, 'L': {}, 'notes': []}
        fns, order = bdlib.disasm(o)
        S, L = {}, {}
        for n in r['order']:
            if n not in fns:
                S[n] = L[n] = 9999
                continue
            if fns[n] != r['fns'][n]:
                S[n] = ndiff(r['fns'][n], fns[n])
                k = ndiff(loose(r['fns'][n]), loose(fns[n]))
                if k:
                    L[n] = k
        for n in order:
            if n not in r['fns']:
                S[n] = L[n] = 9999
        notes = [s for s in ('.text', '.data', '.rdata', '.bss') if bdlib.section(o, s) != r['sec'][s]]
        return {'identical': not S and not notes, 'S': S, 'L': L, 'notes': notes}
    finally:
        bdlib.cleanup(d)


def fnspan(text, head):
    i = text.index('\n' + head) + 1
    j = text.index('\n}\n', i)
    return i, j + 3


def sub(text, old, new, count=-1):
    if old not in text:
        raise ValueError('not found: %r' % old[:70])
    return text.replace(old, new, count)


def main():
    a = sys.argv[1:]
    top, keep, focus = 30, None, None
    if '-n' in a:
        i = a.index('-n'); top = int(a[i + 1]); del a[i:i + 2]
    if '-k' in a:
        i = a.index('-k'); keep = a[i + 1]; del a[i:i + 2]
    if '-f' in a:
        i = a.index('-f'); focus = a[i + 1].split(','); del a[i:i + 2]
    spec = importlib.util.spec_from_file_location('gen', a[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    focus = focus or getattr(m, 'FOCUS', None)
    base = bdlib.read_src(os.path.join(bdlib.R, getattr(m, 'BASE', 'src/build.c')))
    if hasattr(m, 'PRE'):
        base = m.PRE(base)
    cases = m.CASES(base)
    print(len(cases), 'cases', flush=True)

    def one(c):
        lab, f = c
        try:
            t = f(base) if callable(f) else f
        except ValueError as e:
            return lab, {'err': str(e)}, None
        if t is None:
            return lab, {'err': 'skip'}, None
        if t == base:  # an edit whose text wasn't found scores IDENTICAL: gen_bd120 fooled me once
            lab += ' (NO CHANGE)'
        return lab, score(t), t
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, cases))

    def key(x):
        r = x[1]
        if 'err' in r:
            return (10**9, 0)
        if r['identical']:
            return (-1, -1)
        if focus:
            return (sum(v for k, v in r['L'].items() if '_' + k.lstrip('_') in focus or k in focus), sum(v for k, v in r['S'].items() if k in focus))
        return (sum(r['L'].values()), sum(r['S'].values()))
    res.sort(key=key)
    for lab, r, t in res[:top]:
        if 'err' in r:
            print('ERR', lab, r['err'][:200])
        elif r['identical']:
            print('IDENTICAL', lab)
        else:
            print('L%d S%d | %s | %s %s' % (sum(r['L'].values()), sum(r['S'].values()), lab,
                                           ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])))
    name = os.path.splitext(os.path.basename(a[0]))[0]
    pick = [x for x in res if x[0] == keep][0] if keep else res[0]
    if pick[2]:
        open(os.path.join(bdlib.BUILD, name + '_best.c'), 'w', newline='\n').write(pick[2])
        print('wrote build/bd/%s_best.c from %s' % (name, pick[0]))


if __name__ == '__main__':
    main()
