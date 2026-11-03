"""python tools/wip/dehint/nrdef.py <generator.py>: nrsweep's V and C for each variant, plus the clone's measured IRA margin.
margin = got's MEM - class cost - 0.8*(f1+f2), f1/f2 being the freq of the loop's select and recv blocks; the clone's registers need
margin > 0 (flip without asm: -50). Sorted by V+C, then margin. Sources in build/nr/<gen>/."""
import concurrent.futures as cf, glob, importlib.util, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrsweep
BIN, ROOT = nrsweep.BIN, nrsweep.ROOT


def margin(path):
    d = path[:-2] + '.d'
    os.makedirs(d, exist_ok=True)
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-I', os.path.join(ROOT, 'src'), '-O3', '-fno-asynchronous-unwind-tables',
                    '-fdump-rtl-ira-details-blocks', os.path.abspath(path), '-dumpbase', 'a.c', '-o', 'a.s'],
                   cwd=d, env=env, capture_output=True, stdin=subprocess.DEVNULL)

    def clone(pat):
        t = open(glob.glob(os.path.join(d, pat))[0]).read()
        i = t.find(';; Function netRecvVerbose.constprop')
        if i < 0:
            return None
        j = t.find('\n;; Function', i + 10)
        return t[i:j if j > 0 else len(t)]
    s = clone('*r.ira')
    if not s:
        return None, 'no clone'
    hot = {}
    for m in re.finditer(r';; basic block \d+, loop depth (\d+), count \d+, freq (\d+).*?(?=;; basic block|\Z)', s, re.S):
        for c in ('select', 'recv'):
            if m.group(1) != '0' and '[0 %s S1' % c in m.group(0):
                hot[c] = int(m.group(2))
    hot = list(hot.values())
    costs = re.findall(r'a\d+\(r(\d+),l0\) costs:.*?GENERAL_REGS:-?\d+,(-?\d+) MEM:-?\d+,(-?\d+)', s)
    got = None
    for m in re.finditer(r'\(reg/v:SI (\d+) \[ got \]\)', s):
        got = m.group(1)
        break
    last = [c for c in costs if c[0] == got]
    if not last:
        return None, 'no got'
    cl, mem = int(last[-1][1]), int(last[-1][2])
    return mem - cl - int(.8 * sum(hot)), 'MEM %d class %d f %s' % (mem, cl, hot)


def one(item):
    r = nrsweep.run(item)
    try:
        mg, info = margin(item[2])
    except Exception as e:
        mg, info = None, repr(e)[:80]
    return r, mg, info


def main():
    gen = sys.argv[1]
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = os.path.join(ROOT, 'build', 'nr', name)
    os.makedirs(out, exist_ok=True)
    items, seen = [], set()
    for v in m.variants():
        repl = tuple(v[2]) if len(v) > 2 else ()
        if (v[1], repl) in seen:
            continue
        seen.add((v[1], repl))
        items.append((v[0], v[1], os.path.join(out, 'v%d.c' % len(items)), list(repl)))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = list(ex.map(one, items))
    res.sort(key=lambda x: (x[0][0], -(x[1] if x[1] is not None else -10 ** 6)))
    groups = {}
    for r, mg, info in res:
        v = r[1] if r[1] < 10 ** 5 else 'X'
        c = r[2] if r[2] < 10 ** 5 else 'X'
        k = 'V=%s C=%s r=%s margin=%s %s' % (v, c, r[7:9] if len(r) > 7 else '', mg, info)
        groups.setdefault(k, []).append(r[3] + ' ' + os.path.basename(r[6]))
    for k, tags in list(groups.items())[:int(os.environ.get('NR_TOP', '60'))]:
        print(k, '| x%d e.g.' % len(tags), tags[0])


if __name__ == '__main__':
    main()
