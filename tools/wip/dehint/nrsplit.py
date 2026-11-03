"""Sweep netRecv as its OWN source function (attempt 3: not an IPA-CP clone).

python tools/wip/dehint/nrsplit.py <generator.py> [-v N]

The generator defines variants() yielding (tag, netRecv_source[, verbose_source]).
netRecv_source goes before netFree in drafts/net_netRecvVerbose_side.c (whose
netRecvVerbose is used unless verbose_source is given); the netRecv macro goes.
Outputs in build/nr/<gen>/.  Prints N (netRecv lines), V (netRecvVerbose lines),
r= the same with registers erased.  Plain -O3 via fncmp, no flags.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'tools', 'wip', 'dehint', 'drafts', 'net_netRecvVerbose_side.c')).read()
BASE = BASE.replace('#define netRecv(len) netRecvVerbose(len, 0)\n', '')
VS = BASE.index('uint8_t *netRecvVerbose(int *len, uint32_t verbose)')
VE = BASE.index('/* send a length-prefixed block */')
FREE = BASE.index('void netFree(void *p)')


def rdiff(o):
    a, b = {}, {}
    for l in o.split('\n'):
        if re.match(r'^[-+][^-+]', l):
            k = re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:])
            d = a if l[0] == '-' else b
            d[k] = d.get(k, 0) + 1
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def cmp1(path, asm, name):
    env = dict(os.environ, FNCMP_ASM=asm)
    r = subprocess.run([sys.executable, FNCMP, path, name], capture_output=True, text=True, cwd=ROOT, env=env)
    o = (r.stdout + r.stderr).strip()
    if o == 'MATCH':
        return 0, 0, o
    if not o.startswith('---'):
        return 10 ** 5, 10 ** 5, o[:300]
    return len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)]), rdiff(o), o


def run(item):
    tag, nsrc, vsrc, path = item
    text = BASE[:FREE] + nsrc.strip('\n') + '\n\n' + BASE[FREE:VS] + (vsrc.strip('\n') + '\n\n' if vsrc else BASE[VS:VE]) + BASE[VE:]
    open(path, 'w', newline='\n').write(text)
    asm = path[:-2] + '.s'
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables',
                        '-O3', '-I', os.path.join(ROOT, 'src'), path, '-o', asm],
                       env=env, capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        return (10 ** 6, 10 ** 6, 10 ** 6, tag, r.stderr[:300], '', path, 0, 0)
    n, nr, no = cmp1(path, asm, 'netRecv')
    v, vr, vo = cmp1(path, asm, 'netRecvVerbose')
    return (n + v, n, v, tag, no, vo, path, nr, vr)


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
    for x in m.variants():
        vs = x[2] if len(x) > 2 else None
        if (x[1], vs) in seen:
            continue
        seen.add((x[1], vs))
        items.append((x[0], x[1], vs, os.path.join(out, 'v%d.c' % len(items))))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: r[:2])
    hist = {}
    for r in res:
        hist[(r[1], r[2])] = hist.get((r[1], r[2]), 0) + 1
    print('hist N,V', sorted(hist.items())[:30])
    for r in res[:int(os.environ.get('NR_TOP', '20'))]:
        print('N=%s V=%s r=(%s,%s)' % (r[1], r[2], r[7], r[8]), r[3], os.path.basename(r[6]))
    for r in res[:verbose]:
        print('=====', r[0], r[3], r[6])
        print(r[4])
        print(r[5])


if __name__ == '__main__':
    main()
