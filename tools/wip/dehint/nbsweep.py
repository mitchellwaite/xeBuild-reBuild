"""Sweep whole-file variants of src/net.c against build/obj/net.o (plain -O3, as build.sh).

python tools/wip/dehint/nbsweep.py <generator.py> [-n TOP] [-k]

The generator defines variants() yielding (tag, text): the whole net.c.  Gens get the
current source as BASE (import it from here: `from nbsweep import BASE, sub`).
Each is compiled into build/nb/<gen>/<n>.o; .text is disassembled without addresses
(jump/call targets reduced to their symbol, padding kept, so .p2align differences
count), split per function and diffed with the reference.  .rdata/.data are compared
too.  Prints total differing lines, data lines and the functions that differ, best
first.  -k keeps the sources (always kept for rows at 0).
"""
import concurrent.futures as cf, difflib, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
ENV = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
OD = os.path.join(BIN, 'objdump.exe')
GCC = os.path.join(BIN, 'gcc.exe')
REF = os.path.join(ROOT, 'build', 'obj', 'net.o')
BASE = open(os.path.join(ROOT, 'src', 'net.c')).read()


def sub(text, old, new, count=1):
    """replace exactly `count` occurrences of old (error if the count differs)"""
    if text.count(old) != count:
        raise ValueError('expected %d of %r, found %d' % (count, old[:60], text.count(old)))
    return text.replace(old, new)


def funcs(o):
    a = subprocess.run([OD, '-d', '--no-show-raw-insn', '-r', '-M', 'intel', '-j', '.text', o],
                       env=ENV, capture_output=True, text=True).stdout
    out, cur = {}, None
    for l in a.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(\S+)>:$', l)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is None or not l.strip():
            continue
        l = re.sub(r'^\s*[0-9a-f]+:\s*', '', l)
        l = re.sub(r'\b[0-9a-f]+ <([^>+]+)(\+0x[0-9a-f]+)?>', r'<\1>', l)
        out[cur].append(l)
    # gcc numbers the clone (.constprop.N); compare it under one name
    return {re.sub(r'\.constprop\.\d+', '.constprop', k): v for k, v in out.items()}


def data(o):
    b = subprocess.run([OD, '-s', '-j', '.rdata', '-j', '.data', o], env=ENV, capture_output=True, text=True).stdout
    return b.split('\n')[3:]


def ndiff(a, b):
    return sum(1 for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---'))


REF_F = REF_D = None


def run(item):
    i, tag, text, d, keep = item
    c = os.path.join(d, '%d.c' % i)
    o = os.path.join(d, '%d.o' % i)
    open(c, 'w', newline='\n').write(text)
    r = subprocess.run([GCC, '-c', '-O3', '-I', os.path.join(ROOT, 'src'), c, '-o', o], env=ENV, capture_output=True, text=True)
    if r.returncode:
        return (10 ** 6, 0, tag, 'ERROR ' + r.stderr[:200], c)
    f = funcs(o)
    per = {}
    for k in set(f) | set(REF_F):
        n = ndiff(REF_F.get(k, []), f.get(k, []))
        if n:
            per[k] = n
    dd = ndiff(REF_D, data(o))
    tot = sum(per.values())
    os.remove(o)
    if tot or dd:
        if not keep:
            os.remove(c)
    return (tot, dd, tag, ' '.join('%s=%d' % (k.lstrip('_'), v) for k, v in sorted(per.items())), c)


def main():
    global REF_F, REF_D
    gen = sys.argv[1]
    top = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 30
    keep = '-k' in sys.argv
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location('gen', gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    name = os.path.splitext(os.path.basename(gen))[0]
    d = os.path.join(ROOT, 'build', 'nb', name)
    os.makedirs(d, exist_ok=True)
    REF_F, REF_D = funcs(REF), data(REF)
    items = [(i, t, s, d, keep) for i, (t, s) in enumerate(m.variants())]
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items))
    for tot, dd, tag, per, c in res[:top]:
        print('%4d d%-3d %-40s %s  %s' % (tot, dd, tag, per, os.path.relpath(c, ROOT) if os.path.exists(c) else ''))
    print('%d variants, %d at 0' % (len(res), sum(1 for r in res if r[0] == 0 and r[1] == 0)))


if __name__ == '__main__':
    main()
