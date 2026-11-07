"""python tools/wip/dehint/bddup.py <gen.py> [-n TOP] [-f fn,fn] [-k label]: bdrun.py's scoring plus loadBlFiles' bbro
duplications (attempt 28: exp_t10's near miss is one `Duplicated bb` away).

For each case prints loose/strict over FOCUS (or -f) like bdrun.py, then every `Duplicated bb X` line of loadBlFiles' bbro
dump with the frequency of the trace end that was copied into (`Connection: A X` just before it, A's [freq] from the trace
list).  Writes build/bd/<gen>_best.c like bdrun.py."""
import importlib.util, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun


def dups(text, fn='loadBlFiles'):
    d = None
    try:
        ok, o, d = bdlib.compile_src(text, bdlib.P98, extra=['-fdump-rtl-bbro-details'])
        if not ok:
            return 'ERR'
        f = [x for x in os.listdir(d) if x.endswith('.bbro')]
        if not f:
            return '?'
        t = open(os.path.join(d, f[0]), errors='replace').read()
        i = t.find(';; Function %s ' % fn)
        j = t.find(';; Function ', i + 10)
        t = t[i:j if j > 0 else None]
        freq = {}
        for m in re.finditer(r'^Trace \d+ \(round \d\):(.*)$', t, re.M):
            for b, fq in re.findall(r'(\d+) \[(\d+)\]', m.group(1)):
                freq[b] = fq
        out = []
        last = None
        for line in t.splitlines():
            m = re.match(r'Connection: (\d+) (\d+)', line)
            if m:
                last = m.group(1)
            m = re.match(r'Duplicated bb (\d+)', line)
            if m:
                out.append('dup %s<-%s[%s]' % (m.group(1), last, freq.get(last, '?')))
        return ' '.join(out) or 'nodup'
    finally:
        if d:
            bdlib.cleanup(d)


def main():
    a = sys.argv[1:]
    top, keep, focus = 40, None, None
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
            return lab, {'err': str(e)}, None, ''
        if t is None:
            return lab, {'err': 'skip'}, None, ''
        if t == base:
            lab += ' (NO CHANGE)'
        return lab, bdrun.score(t), t, dups(t)
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
    for lab, r, t, dp in res[:top]:
        if 'err' in r:
            print('ERR', lab, r['err'][:200])
        elif r['identical']:
            print('IDENTICAL', lab, '|', dp)
        else:
            print('L%d S%d | %s | %s %s | %s' % (sum(r['L'].values()), sum(r['S'].values()), lab,
                                                ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes']), dp))
    name = os.path.splitext(os.path.basename(a[0]))[0]
    pick = [x for x in res if x[0] == keep][0] if keep else res[0]
    if pick[2]:
        open(os.path.join(bdlib.BUILD, name + '_best.c'), 'w', newline='\n').write(pick[2])
        print('wrote build/bd/%s_best.c from %s' % (name, pick[0]))


if __name__ == '__main__':
    main()
