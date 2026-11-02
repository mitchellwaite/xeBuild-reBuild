"""Sweep readFileIn shapes against the original (plain -O3, no flags).

python tools/wip/dehint/rfsweep.py <generator.py> [-v N] [-k]

The generator module defines variants(), yielding (tag, source) where source is
the whole definition of readFileIn plus anything it needs before it.  Each one
replaces the hinted readFileIn (and rf_hint/rf_sink) in src/fileutil.c, is written
to build/rf/<genname>/ and compared with tools/re/fncmp.py.  Prints a histogram and
the best tags; -v N prints the N best diffs; -k keeps every source (default:
only the best 20).  Compile errors count as ERROR, never as a match.
"""
import concurrent.futures as cf, difflib, importlib.util, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'fileutil.c')).read()
START = BASE.index('/*\n * readFileIn:')
END = BASE.index('unsigned int calcConfigSum')


def rdiff(o):
    """differing lines once registers are erased: how far the shape is, ignoring allocation"""
    a, b = {}, {}
    for l in o.split('\n'):
        if re.match(r'^[-+][^-+]', l):
            k = re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:])
            d = a if l[0] == '-' else b
            d[k] = d.get(k, 0) + 1
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def sdiff(o):
    """sequence diff with registers erased: layout and shape differences only"""
    ref, mine = [], []
    for l in o.split('\n')[2:]:
        if l.startswith('@@') or not l:
            continue
        if l[0] in ' -':
            ref.append(re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:]))
        if l[0] in ' +':
            mine.append(re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:]))
    return len([l for l in difflib.unified_diff(ref, mine, lineterm='', n=0) if l[0] in '+-' and l[:3] not in ('---', '+++')])


def ira(item):
    """(margin of the buf/return thread over the top thread, tag): -m"""
    tag, src, path, flags = item[:4]
    d = path + '.d'
    os.makedirs(d, exist_ok=True)
    a = os.path.join(d, 'a.c')
    shutil.copy(path, a)
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-O3', '-I', os.path.join(ROOT, 'src'),
                        '-fno-asynchronous-unwind-tables', '-fdump-rtl-ira'] + flags + ['a.c'],
                       cwd=d, env=env, capture_output=True)
    res = None
    for f in os.listdir(d):
        if f.endswith('r.ira'):
            t = open(os.path.join(d, f)).read()
            t = t[t.index(';; Function readFileIn '):]
            t = t[:t.index(';; Function calcConfigSum')]
            names = {}
            for m in re.finditer(r'\(reg(?:/\w+)*:\w+ (\d+)(?: \[ ([^\]]*) \])?', t):
                if m.group(2):
                    names.setdefault(m.group(1), m.group(2).strip())
            th = [(int(m.group(1)), re.findall(r'r(\d+)\(', m.group(2))) for m in re.finditer(r'Result \(freq=(\d+)\): (.*)', t)]
            pops = [names.get(m.group(1), m.group(1)) for m in re.finditer(r'Popping a\d+\(r(\d+),l0\)', t)][:4]
            ret = [f for f, rs in th if any(names.get(x) == '<retval>' for x in rs)]
            top = max(f for f, _ in th)
            res = (ret[0] - top if ret else None, top, tuple(sorted((f for f, _ in th), reverse=True)), tuple(pops))
    shutil.rmtree(d)
    return res, tag, os.path.basename(path)


def run(item):
    tag, src, path, flags = item[:4]
    head = BASE[:START]
    for old, new in (item[4] if len(item) > 4 else []):
        if old not in head:
            return 10 ** 6, tag, 'replacement not found: ' + old, path
        head = head.replace(old, new)
    open(path, 'w', newline='\n').write(head + src.strip('\n') + '\n\n' + BASE[END:])
    r = subprocess.run([sys.executable, FNCMP, path, 'readFileIn', '-O3', '-I', os.path.join(ROOT, 'src')] + flags,
                       capture_output=True, text=True, cwd=ROOT)
    o = (r.stdout + r.stderr).strip()
    if o == 'MATCH':
        return 0, tag, o, path
    if not o.startswith('---'):
        return 10 ** 6, tag, o[:400], path
    return len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)]), tag, o, path


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = os.path.join(ROOT, 'build', 'rf', name)
    os.makedirs(out, exist_ok=True)
    items, seen = [], set()
    for v in m.variants():
        tag, src = v[:2]
        flags = list(v[2]) if len(v) > 2 else []
        key = (src, tuple(flags), tuple(v[3]) if len(v) > 3 else ())
        if key in seen:
            continue
        seen.add(key)
        items.append((tag, src, os.path.join(out, 'v%d.c' % len(items)), flags, list(v[3]) if len(v) > 3 else []))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: r[0])
    if '-m' in sys.argv:
        with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
            mr = list(ex.map(ira, items))
        seen_m = {}
        for r, tag, base in mr:
            if r and r[0] is not None and r[0:2] not in seen_m:
                seen_m[r[0:2]] = (r, tag, base)
        print('IRA margin (ret thread - top thread):')
        for k in sorted(seen_m, reverse=True)[:12]:
            print(' ', seen_m[k])
        firsts = {}
        for r, tag, base in mr:
            if r:
                firsts.setdefault(r[3][:1], []).append((tag, base))
        print('first popped:', {k: (len(v), v[0]) for k, v in firsts.items()})
    hist = {}
    for n, *_ in res:
        hist[n] = hist.get(n, 0) + 1
    print('hist', sorted(hist.items())[:15])
    keep = {r[3] for r in res if r[0] < 10 ** 6 and '-xor edi,edi' not in r[2] and '-mov ebx,eax' not in r[2]} | {r[3] for r in res if r[0] < 10 ** 6 and '-jae' not in r[2]} | {r[3] for r in res[:20]} | {r[3] for r in sorted((r for r in res if r[0] < 10 ** 6), key=lambda r: rdiff(r[2]))[:15]} | {r[3] for r in sorted((r for r in res if r[0] < 10 ** 6), key=lambda r: sdiff(r[2]))[:25]}
    if '-k' not in sys.argv:
        for r in res:
            if r[3] not in keep and os.path.exists(r[3]):
                os.remove(r[3])
    for n, tag, o, path in res[:25]:
        print(n if n < 10 ** 6 else 'ERROR', 'r=%d' % rdiff(o), tag, os.path.basename(path))
    print('best by sequence diff with registers erased (s=):')
    for s, n, tag, base in sorted((sdiff(r[2]), r[0], r[1], os.path.basename(r[3])) for r in res if r[0] < 10 ** 6)[:25]:
        print('s=%d' % s, n, tag, base)
    good = [r for r in res if r[0] < 10 ** 6 and '-jae' not in r[2]]
    print('cmp order right:', len(good), 'best:', [(r[0], rdiff(r[2]), r[1], os.path.basename(r[3])) for r in good[:10]])
    regs = [r for r in res if r[0] < 10 ** 6 and '-xor edi,edi' not in r[2] and '-mov ebx,eax' not in r[2]]
    print('size/buf registers right:', len(regs), [(r[0], rdiff(r[2]), r[1], os.path.basename(r[3])) for r in regs[:12]])
    print('best by register-free diff:')
    for n, tag, o, path in sorted((r for r in res if r[0] < 10 ** 6), key=lambda r: rdiff(r[2]))[:15]:
        print(n, 'r=%d' % rdiff(o), tag, os.path.basename(path))
    for n, tag, o, path in res[:verbose]:
        print('=====', n, tag, path)
        print(o)


if __name__ == '__main__':
    main()
