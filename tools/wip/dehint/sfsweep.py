"""Sweep stfsGetFile shapes against the original (plain -O3, no flags).

python tools/wip/dehint/sfsweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source[, repl]): source replaces
stfsGetFile in src/stfs.c; repl is a list of (old, new) text replacements on the
whole file.  Outputs go to build/sf/<gen>/, compared with tools/re/fncmp.py.
Prints the histogram and the best tags: lines, and lines with registers erased.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'stfs.c')).read()
START = BASE.index('int stfsGetFile(stfs_t *c')
END = BASE.index('void stfsInit(stfs_t *c)')


def rdiff(o):
    a, b = {}, {}
    for l in o.split('\n'):
        if re.match(r'^[-+][^-+]', l):
            k = re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:])
            d = a if l[0] == '-' else b
            d[k] = d.get(k, 0) + 1
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def run(item):
    tag, src, path, repl = item
    text = BASE[:START] + src.strip('\n') + '\n\n' + BASE[END:]
    for old, new in repl:
        if old not in text:
            return 10 ** 6, tag, 'replacement not found: ' + old, path
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    r = subprocess.run([sys.executable, FNCMP, path, 'stfsGetFile', '-O3', '-I', os.path.join(ROOT, 'src')],
                       capture_output=True, text=True, cwd=ROOT)
    o = (r.stdout + r.stderr).strip()
    if o == 'MATCH':
        return 0, tag, o, path
    if not o.startswith('---'):
        return 10 ** 6, tag, o[:300], path
    return len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)]), tag, o, path


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = os.path.join(ROOT, 'build', 'sf', name)
    os.makedirs(out, exist_ok=True)
    items, seen = [], set()
    for v in m.variants():
        tag, src = v[:2]
        repl = list(v[2]) if len(v) > 2 else []
        key = (src, tuple(repl))
        if key not in seen:
            seen.add(key)
            items.append((tag, src, os.path.join(out, 'v%d.c' % len(items)), repl))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(max_workers=os.cpu_count()) as ex:
        res = list(ex.map(run, items))
    res.sort(key=lambda r: (r[0], rdiff(r[2]) if r[0] < 10 ** 6 else 0))
    hist = {}
    for r in res:
        hist[r[0]] = hist.get(r[0], 0) + 1
    print('lines:', ' '.join('%d:%d' % kv for kv in sorted(hist.items())[:14]))
    for r in res[:12]:
        print('%7d r=%-3d %s  %s' % (r[0], rdiff(r[2]) if r[0] < 10 ** 6 else -1, r[1], os.path.relpath(r[3], ROOT)))
    errs = [r for r in res if r[0] >= 10 ** 6]
    if errs:
        print('error sample:', errs[0][1], errs[0][2])
    for r in res[:verbose]:
        print(r[1])
        print(r[2])


if __name__ == '__main__':
    main()
