"""Sweep sendAvatarData shapes against the original (plain -O3, no flags).

python tools/wip/dehint/casweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source[, repl]): source replaces
prepSysex and sendAvatarData in src/console_hdd.c (from `int prepSysex` up to
`int sendDir`); repl is a list of (old, new) text replacements on the whole file.
Goes to build/ca/<gen>/ and is compared with tools/re/fncmp.py.  Prints the
histogram and the best tags, by lines and by lines with registers erased.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'console_hdd.c')).read()
START = BASE.index('int prepSysex(void)')
END = BASE.index('int sendDir(const char *src')


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
    # CA_DIAG=<p>: diagnostic only, expect on netMount at probability p (never a result)
    diag = []
    if os.environ.get('CA_DIAG'):
        text = re.sub(r'if \(netMount\(SYSEX, "(.*?)"\)\)', lambda m: 'if (__builtin_expect(netMount(SYSEX, "%s"), 1))' % m.group(1), text)
        diag = ['--param', 'builtin-expect-probability=' + os.environ['CA_DIAG']]
    open(path, 'w', newline='\n').write(text)
    r = subprocess.run([sys.executable, FNCMP, path, 'sendAvatarData', '-O3', '-I', os.path.join(ROOT, 'src')] + diag,
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
    out = os.path.join(ROOT, 'build', 'ca', name)
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
    with open(os.path.join(out, 'results.txt'), 'w', newline='\n') as f:  # every row: lines, r, tag, file
        for n, tag, o, path in res:
            f.write('%d r=%d %s %s\n' % (n, rdiff(o), tag, os.path.basename(path)))
    hist = {}
    for n, *_ in res:
        hist[n] = hist.get(n, 0) + 1
    print('hist', sorted(hist.items())[:15])
    for n, tag, o, path in res[:25]:
        print(n if n < 10 ** 6 else 'ERROR', 'r=%d' % rdiff(o), tag, os.path.basename(path), '' if n < 10 ** 6 else o)
    im = [r for r in res if r[0] < 10 ** 6 and ('-imul' not in r[2] or '+imul' in r[2])]
    print('imul kept:', len(im), [(r[0], rdiff(r[2]), r[1], os.path.basename(r[3])) for r in im[:15]])
    xo = [r for r in res if r[0] < 10 ** 6 and '+xor ebp,ebp' not in r[2] and ('-imul' not in r[2] or '+imul' in r[2])]
    print('imul and guard xor right:', len(xo), [(r[0], rdiff(r[2]), r[1], os.path.basename(r[3])) for r in xo[:15]])
    print('best register-free:')
    for n, tag, o, path in sorted((r for r in res if r[0] < 10 ** 6), key=lambda r: rdiff(r[2]))[:10]:
        print(n, 'r=%d' % rdiff(o), tag, os.path.basename(path))
    for n, tag, o, path in res[:verbose]:
        print('=====', n, tag, path)
        print(o)


if __name__ == '__main__':
    main()
