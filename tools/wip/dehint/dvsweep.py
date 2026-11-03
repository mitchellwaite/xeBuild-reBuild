"""Sweep daeVerifySig/verifyDae shapes against the hinted build (plain -O3, no flags).

python tools/wip/dehint/dvsweep.py <generator.py> [-v N]

The generator defines variants() yielding (tag, source[, repl]): source replaces
everything from `static void hint` up to (not including) `int fcrtVerifySig(uint8_t *fcrt)\n{`
in src/bootloaders.c; repl is a list of (old, new) on the whole file.
Output in build/dv/<gen>/.  Columns:
  n   differing lines of daeVerifySig + verifyDae (function text, labels and .p2align
      included, as a line-set multiset diff)
  dv, vd  each one's share
  o   other bootloaders functions whose text changed
  rd  1 when the whole .rdata string list and order equal the reference's
The reference is commit 5c78c82's src/bootloaders.c (the hinted functions, byte-identical
to the original), kept in build/dv/hinted_bootloaders.c.
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
HINTED = os.path.join(ROOT, 'build', 'dv', 'hinted_bootloaders.c')
os.makedirs(os.path.dirname(HINTED), exist_ok=True)
if not os.path.exists(HINTED):
    # the last commit with the hinted daeVerifySig
    with open(HINTED, 'wb') as f:
        f.write(subprocess.run(['git', 'show', '5c78c82:src/bootloaders.c'], cwd=ROOT, capture_output=True, check=True).stdout)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = open(HINTED).read()
START = BASE.index('static void hint(int *p)')
END = BASE.index('int fcrtVerifySig(uint8_t *fcrt)\n{')


def funcs(s):
    out, cur = {}, None
    for l in s.split('\n'):
        m = re.match(r'^(_\w+(?:\.\w+)*):$', l)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur:
            if re.match(r'\s*\.(def|globl)\b', l) or l.strip().startswith('.ident'):
                cur = None
            else:
                out[cur].append(l)
    lits = {}
    for m in re.finditer(r'^(LC\d+):\n\s*\.ascii (".*")$', s, re.M):
        lits[m.group(1)] = m.group(2)
    for k, v in out.items():
        names, new = {}, []
        for l in v:
            l = re.sub(r'\bLC\d+\b', lambda m: lits.get(m.group(0), m.group(0)), l)
            new.append(re.sub(r'\bL\d+\b', lambda m: names.setdefault(m.group(0), 'X%d' % len(names)), l))
        out[k] = new
    return out, re.findall(r'^\s*\.ascii (".*")$', s, re.M)


def compile_to(path, asm, extra=()):
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    return subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables',
                           '-O3'] + list(extra) + ['-I', os.path.join(ROOT, 'src'), path, '-o', asm],
                          env=env, capture_output=True, text=True, cwd=ROOT)


def udiff(a, b):
    import difflib
    return [l for l in difflib.unified_diff(a, b, lineterm='', n=1) if not l.startswith(('---', '+++'))]


def nd(a, b):
    return len([l for l in udiff(a or [], b or []) if l[0] in '+-'])


def run(item):
    tag, src, path, repl, ref, rrd = item
    text = BASE[:START] + src.strip('\n') + '\n\n' + BASE[END:]
    for old, new in repl:
        if old not in text:
            return (10 ** 6, 0, 0, 0, 0, tag, 'replacement not found: ' + old, path)
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    asm = path[:-2] + '.s'
    r = compile_to(path, asm)
    if r.returncode:
        return (10 ** 6, 0, 0, 0, 0, tag, r.stderr[:400], path)
    f, rd = funcs(open(asm).read())
    dv = nd(ref['_daeVerifySig'], f.get('_daeVerifySig'))
    vd = nd(ref['_verifyDae'], f.get('_verifyDae'))
    other = sum(1 for k in ref if k not in ('_daeVerifySig', '_verifyDae') and f.get(k) != ref[k])
    d = '\n'.join(udiff(ref['_daeVerifySig'], f.get('_daeVerifySig') or []) + ['=== verifyDae'] +
                  udiff(ref['_verifyDae'], f.get('_verifyDae') or []))
    if rd != rrd:
        d += '\n=== rdata\n' + '\n'.join(l[:50] for l in udiff(rrd, rd))
    return (dv + vd, dv, vd, other, int(rd == rrd), tag, d, path)


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = os.path.join(ROOT, 'build', 'dv', name)
    os.makedirs(out, exist_ok=True)
    refc = os.path.join(out, 'ref.c')
    open(refc, 'w', newline='\n').write(BASE)
    compile_to(refc, refc[:-2] + '.s')
    ref, rrd = funcs(open(refc[:-2] + '.s').read())
    items, seen = [], set()
    for v in m.variants():
        rp = tuple(v[2]) if len(v) > 2 else ()
        if (v[1], rp) in seen:
            continue
        seen.add((v[1], rp))
        items.append((v[0], v[1], os.path.join(out, 'v%d.c' % len(items)), list(rp), ref, rrd))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: (r[0], -r[4], r[3]))
    hist = {}
    for r in res:
        hist[r[0]] = hist.get(r[0], 0) + 1
    print('hist', sorted(hist.items())[:30])
    for r in res[:int(os.environ.get('WB_TOP', '30'))]:
        print(r[0], 'dv=%s vd=%s o=%s rd=%s' % (r[1], r[2], r[3], r[4]), r[5], os.path.basename(r[7]))
    for r in res[:verbose]:
        print('=====', r[0], r[5], r[7])
        print(r[6])


if __name__ == '__main__':
    main()
