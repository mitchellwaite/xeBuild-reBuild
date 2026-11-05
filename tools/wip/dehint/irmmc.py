"""python tools/wip/dehint/irmmc.py <gen.py> : for every variant of a generator, the zeropair test's probability in the optimized dump of copyMmcImage and of loadDump, and each function's loose diff."""
import importlib.util, itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib


def probs(txt, fn):
    i = txt.find(';; Function %s ' % fn)
    if i < 0:
        return '-'
    t = txt[i:]
    j = t.find(';; Function', 10)
    t = t[:j] if j > 0 else t
    for p in re.split(r'(?m)^;;   basic block ', t)[1:]:
        if 'memcmp' in p:
            s = re.findall(r'\[([\d.]+)%\]', p[p.find('succ:'):])
            c = re.search(r'if \((.*)\)', p)
            return '%s %s' % (c.group(1) if c else '?', '/'.join(s))
    return '?'


def one(a):
    lab, text = a
    ok, o, d = irlib.compile_src(text, [], extra=['-fdump-tree-optimized-blocks-details'])
    if not ok:
        return lab, o[:200], '', '', {}
    idn, tot, per, notes = irlib.report(o)
    f = [x for x in os.listdir(d) if x.endswith('optimized')]
    txt = open(os.path.join(d, f[0]), errors='replace').read()
    irlib.cleanup(d)
    return lab, probs(txt, 'copyMmcImage'), probs(txt, 'loadDump'), tot, per


if __name__ == '__main__':
    s = importlib.util.spec_from_file_location('gen', sys.argv[1])
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    text = open(os.path.join(irlib.R, m.BASE), newline='').read().replace('\r\n', '\n')
    args = []
    for c in itertools.product(*m.AXES):
        t = text
        for lab, ed in c:
            for x, y in ed:
                if x not in t:
                    raise ValueError(lab + x[:60])
                t = t.replace(x, y)
        args.append(('+'.join(x[0] for x in c), t))
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, args))
    res.sort(key=lambda r: r[3] if isinstance(r[3], int) else 99999)
    for r in res:
        print(r[3], r[0], '| copy', r[1], '| load', r[2], '|', {k: v for k, v in r[4].items() if k in ('_copyMmcImage', '_loadDump', '_parseDump')})
