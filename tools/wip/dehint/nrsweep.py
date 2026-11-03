"""Sweep netRecvVerbose shapes against the original (plain -O3, no flags).

python tools/wip/dehint/nrsweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source[, repl]): source replaces
netRecvVerbose in src/net.c (up to `#define netRecv(len)`); repl is a list of
(old, new) replacements on the whole file.  Goes to build/nr/<gen>/.  Each is
compiled once and compared twice with tools/re/fncmp.py: as netRecvVerbose and,
for gcc's constprop clone (whatever its number), as netRecv.  Prints a histogram
by total lines: `V` the function's, `C` the clone's (X when gcc made no clone), r=
the same with registers erased.  NR_DIAG="--param builtin-expect-probability=N":
extra flags, diagnostic only.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'net.c')).read()
START = BASE.index('uint8_t *netRecvVerbose(int *len, uint32_t verbose)')
END = BASE.index('#define netRecv(len)')
DIAG = os.environ.get('NR_DIAG', '').split()


def rdiff(o):
    a, b = {}, {}
    for l in o.split('\n'):
        if re.match(r'^[-+][^-+]', l):
            k = re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:])
            d = a if l[0] == '-' else b
            d[k] = d.get(k, 0) + 1
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def cmp1(path, asm, name, sym=None):
    env = dict(os.environ, FNCMP_ASM=asm)
    if sym:
        env['FNCMP_GCCSYM'] = sym
    r = subprocess.run([sys.executable, FNCMP, path, name], capture_output=True, text=True, cwd=ROOT, env=env)
    o = (r.stdout + r.stderr).strip()
    if o == 'MATCH':
        return 0, 0, o
    if not o.startswith('---'):
        return 10 ** 5, 10 ** 5, o[:300]
    return len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)]), rdiff(o), o


def run(item):
    tag, src, path, repl = item
    text = BASE[:START] + src.strip('\n') + '\n\n' + BASE[END:]
    for old, new in repl:
        if old not in text:
            return (10 ** 6, 0, 0, tag, 'replacement not found: ' + old, '', path)
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    asm = path[:-2] + '.s'
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables',
                        '-O3', '-I', os.path.join(ROOT, 'src')] + DIAG + [path, '-o', asm],
                       env=env, capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        return (10 ** 6, 0, 0, tag, r.stderr[:300], '', path)
    s = open(asm).read()
    m = re.search(r'^(_netRecvVerbose\.constprop\.\d+):', s, re.M)
    v, vr, vo = cmp1(path, asm, 'netRecvVerbose')
    if m:
        c, cr, co = cmp1(path, asm, 'netRecv', m.group(1))
    else:
        c, cr, co = 10 ** 5, 10 ** 5, 'no clone'
    return (v + c, v, c, tag, vo, co, path, vr, cr)


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
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
        res = sorted(ex.map(run, items), key=lambda r: (r[0], r[1]))
    hist = {}
    for r in res:
        k = (r[1] if r[1] < 10 ** 5 else 'X', r[2] if r[2] < 10 ** 5 else 'X')
        hist[k] = hist.get(k, 0) + 1
    print('hist V,C', sorted(hist.items(), key=lambda kv: str(kv[0]))[:30])
    def show(r):
        rr = (r[7], r[8]) if len(r) > 7 else ''
        print(r[0] if r[0] < 10 ** 5 else 'X', 'V=%s C=%s r=%s' % (r[1], r[2] if r[2] < 10 ** 5 else 'X', rr), r[3], os.path.basename(r[6]))
    for r in res[:int(os.environ.get("NR_TOP", "20"))]:
        show(r)
    print('best V:')
    for r in sorted(res, key=lambda r: r[1])[:8]:
        show(r)
    print('best C:')
    for r in sorted(res, key=lambda r: r[2])[:8]:
        show(r)
    print('best V+C registers erased:')
    for r in sorted((r for r in res if len(r) > 7), key=lambda r: r[7] + r[8])[:8]:
        show(r)
    for r in res[:verbose]:
        print('=====', r[0], r[3], r[6])
        print(r[4])
        print(r[5])


if __name__ == '__main__':
    main()
