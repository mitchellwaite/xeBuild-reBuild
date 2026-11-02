"""Sweep myatou32 shapes against the original (plain -O3, no flags).

python tools/wip/dehint/musweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source): the whole definition of
myatou32 plus anything it needs before it.  It replaces myatou32 in src/fileutil.c
(the comment above it and the function), goes to build/mu32/<gen>/ and is compared
with tools/re/fncmp.py.  Prints the histogram and the best tags.  Compile errors
count as ERROR.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'fileutil.c')).read()
START = BASE.index('// converts a decimal or 0x-prefixed')
END = BASE.index('uint32_t myatoh32(const char* dat')


def run(item):
    tag, src, path, repl = item
    text = BASE[:START] + src.strip('\n') + '\n\n' + BASE[END:]
    for old, new in repl:
        if old not in text:
            return 10 ** 6, tag, 'replacement not found: ' + old, path
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    r = subprocess.run([sys.executable, FNCMP, path, 'myatou32', '-O3', '-I', os.path.join(ROOT, 'src')],
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
    out = os.path.join(ROOT, 'build', 'mu32', name)
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
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: r[0])
    hist = {}
    for n, *_ in res:
        hist[n] = hist.get(n, 0) + 1
    print('hist', sorted(hist.items())[:20])
    for n, tag, o, path in res[:30]:
        print(n if n < 10 ** 6 else 'ERROR', tag, os.path.basename(path))
    for n, tag, o, path in res[:verbose]:
        print('=====', n, tag, path)
        print(o)


if __name__ == '__main__':
    main()
