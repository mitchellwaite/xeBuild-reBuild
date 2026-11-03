"""Sweep netWritePatches shapes against the original (plain -O3, no flags).

python tools/wip/dehint/pwsweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source[, repl]): source replaces
netWritePatches in src/net.c; repl is a list of (old, new)
replacements on the whole file.  Goes to build/pw/<gen>/.  Prints differing lines,
r= with registers erased, o= other net functions whose text changed compared with
src/net.c's own output, a=1 when netWritePatches's whole .s text (.p2align and jump targets included, which fncmp
doesn't see) equals the hinted build's, which is the reference byte for byte.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'net.c')).read()
START = BASE.index('int netWritePatches(')
END = len(BASE)
FN = 'netWritePatches'
PARAM = []


def rdiff(o):
    a, b = {}, {}
    for l in o.split('\n'):
        if re.match(r'^[-+][^-+]', l):
            k = re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', l[1:])
            d = a if l[0] == '-' else b
            d[k] = d.get(k, 0) + 1
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def funcs(s):
    out, cur = {}, None
    for l in s.split('\n'):
        m = re.match(r'^(_\w+(?:\.\w+)*):$', l)
        if m and not m.group(1).startswith('_L'):
            cur = m.group(1)
            out[cur] = []
        elif cur:
            if re.match(r'\s*\.def\b', l):
                cur = None
            elif not re.match(r'^L\w*:', l) and not l.strip().startswith('.'):
                out[cur].append(re.sub(r'\bL\w*\d+', 'L', l))
    return out


def aligns(s):
    """netWritePatches's instruction count before each .p2align, the alignment's shape"""
    i = s.find('_' + FN + ':')
    if i < 0:
        return None
    t = s[i:]
    j = t.find('.def', 10)
    out, n = [], 0
    for l in t[:j].split('\n')[1:]:
        l = l.strip()
        if l.startswith('.p2align'):
            out.append((n, l))
        elif l and not l.endswith(':') and not l.startswith('.'):
            n += 1
    return out


def compile_to(path, asm, extra=()):
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    return subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables',
                           '-O3'] + list(extra) + ['-I', os.path.join(ROOT, 'src'), path, '-o', asm],
                          env=env, capture_output=True, text=True, cwd=ROOT)


def run(item):
    tag, src, path, repl, ref, refa = item
    text = BASE[:START] + src.strip('\n') + '\n\n' + BASE[END:]
    for old, new in repl:
        if old not in text:
            return (10 ** 6, 0, 0, 0, tag, 'replacement not found: ' + old, path)
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    asm = path[:-2] + '.s'
    r = compile_to(path, asm)
    if r.returncode:
        return (10 ** 6, 0, 0, 0, tag, r.stderr[:300], path)
    s = open(asm).read()
    f = funcs(s)
    other = sum(1 for k in ref if k != '_' + FN and f.get(k) != ref[k])
    al = int(aligns(s) == refa)
    # the clone is netRecv in the reference; fncmp only sees that after linking
    s = re.sub(r'_netRecvVerbose\.constprop\.\d+', '_netRecv', s)
    open(asm, 'w', newline='\n').write(s)
    env = dict(os.environ, FNCMP_ASM=asm)
    r = subprocess.run([sys.executable, FNCMP, path, FN], capture_output=True, text=True, cwd=ROOT, env=env)
    o = (r.stdout + r.stderr).strip()
    if o == 'MATCH':
        return (0, 0, other, al, tag, o, path)
    if not o.startswith('---'):
        return (10 ** 5, 0, other, al, tag, o[:300], path)
    n = len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    return (n, rdiff(o), other, al, tag, o, path)


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = os.path.join(ROOT, 'build', 'pw', name)
    os.makedirs(out, exist_ok=True)
    # other functions: plain -O3 of src/net.c.  Reference alignment: as build.sh's param.
    refc = os.path.join(out, 'ref.c')
    open(refc, 'w', newline='\n').write(BASE)
    compile_to(refc, refc[:-2] + '.s')
    ref = funcs(open(refc[:-2] + '.s').read())
    compile_to(refc, refc[:-2] + '.p.s', PARAM)
    refa = aligns(open(refc[:-2] + '.p.s').read())
    items, seen = [], set()
    for v in m.variants():
        rp = tuple(v[2]) if len(v) > 2 else ()
        if (v[1], rp) in seen:
            continue
        seen.add((v[1], rp))
        items.append((v[0], v[1], os.path.join(out, 'v%d.c' % len(items)), list(rp), ref, refa))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: (r[0], r[1], -r[3]))
    hist = {}
    for r in res:
        hist[r[0]] = hist.get(r[0], 0) + 1
    print('hist', sorted(hist.items())[:30])
    for r in res[:int(os.environ.get('WB_TOP', '25'))]:
        print(r[0], 'r=%s o=%s a=%s' % (r[1], r[2], r[3]), r[4], os.path.basename(r[6]))
    for r in res[:verbose]:
        print('=====', r[0], r[4], r[6])
        print(r[5])


if __name__ == '__main__':
    main()
