"""Sweep cb/cd/ceDecrypt shapes against the hinted build (plain -O3, no flags).

python tools/wip/dehint/cbsweep.py <generator.py> [-v N] [--dump]

The generator defines variants() yielding (tag, source[, repl]): source replaces the
function FN (default cbDecrypt) in src/bootloaders.c, comment and attribute lines
included; repl is a list of (old, new) on the whole file.  Output in build/cb/<gen>/.
Columns:
  n   differing lines from the original, as fncmp prints them (MATCH = 0)
  a   differing lines of the function's whole .s text against the hinted build's (the
      reference byte for byte): labels numbered by first use, literals by contents,
      .p2align included.  fncmp doesn't see those.
  o   other bootloaders functions whose text changed
  rd  1 when the object's whole string list and order equal the reference's
The reference is src/bootloaders.c as of commit 28bd769, kept in build/cb/hinted_bootloaders.c.
"""
import concurrent.futures as cf, difflib, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
HINTED = os.path.join(ROOT, 'build', 'cb', 'hinted_bootloaders.c')
os.makedirs(os.path.dirname(HINTED), exist_ok=True)
if not os.path.exists(HINTED):
    with open(HINTED, 'wb') as f:
        f.write(subprocess.run(['git', 'show', '28bd769:src/bootloaders.c'], cwd=ROOT, capture_output=True,
                               check=True).stdout)
BASE = open(HINTED, newline='').read()
BOUNDS = {
    'cbDecrypt': ('/* decrypted copy of a CB/SB', '/* decrypted copy of an SC/SD/CD'),
    'cdDecrypt': ('/* decrypted copy of an SC/SD/CD', '/* decrypted copy of an SE/CE'),
    'ceDecrypt': ('/* decrypted copy of an SE/CE', '/* the object\'s strings'),
}


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
    return [l for l in difflib.unified_diff(a, b, lineterm='', n=1) if not l.startswith(('---', '+++'))]


def run(item):
    tag, src, path, repl, ref, rrd, fn, start, end = item
    text = BASE[:start] + src.strip('\n') + '\n\n' + BASE[end:]
    for old, new in repl:
        if old not in text:
            return (10 ** 6, 0, 0, 0, tag, 'replacement not found: ' + old, path)
        text = text.replace(old, new)
    open(path, 'w', newline='\n').write(text)
    asm = path[:-2] + '.s'
    r = compile_to(path, asm)
    if r.returncode:
        return (10 ** 6, 0, 0, 0, tag, r.stderr[:400], path)
    f, rd = funcs(open(asm).read())
    d = udiff(ref['_' + fn], f.get('_' + fn) or [])
    a = len([l for l in d if l[0] in '+-'])
    other = sum(1 for k in ref if k != '_' + fn and f.get(k) != ref[k])
    env = dict(os.environ, FNCMP_ASM=asm)
    r = subprocess.run([sys.executable, FNCMP, path, fn], capture_output=True, text=True, cwd=ROOT, env=env)
    o = (r.stdout + r.stderr).strip()
    n = 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    txt = o + '\n=== .s\n' + '\n'.join(d)
    if rd != rrd:
        txt += '\n=== rdata\n' + '\n'.join(l[:60] for l in udiff(rrd, rd))
    return (n, a, other, int(rd == rrd), tag, txt, path)


def main():
    gen = sys.argv[1]
    verbose = int(sys.argv[sys.argv.index('-v') + 1]) if '-v' in sys.argv else 0
    name = os.path.splitext(os.path.basename(gen))[0]
    spec = importlib.util.spec_from_file_location(name, gen)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fn = getattr(m, 'FN', 'cbDecrypt')
    start, end = BASE.index(BOUNDS[fn][0]), BASE.index(BOUNDS[fn][1])
    out = os.path.join(ROOT, 'build', 'cb', name)
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
        items.append((v[0], v[1], os.path.join(out, 'v%d.c' % len(items)), list(rp), ref, rrd, fn, start, end))
    print(len(items), 'variants')
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = sorted(ex.map(run, items), key=lambda r: (r[0], r[1], -r[3], r[2]))
    hist = {}
    for r in res:
        hist[r[0]] = hist.get(r[0], 0) + 1
    print('hist', sorted(hist.items())[:30])
    for r in res[:int(os.environ.get('WB_TOP', '30'))]:
        print(r[0], 'a=%s o=%s rd=%s' % (r[1], r[2], r[3]), r[4], os.path.basename(r[6]))
    for r in res[:verbose]:
        print('=====', r[0], r[4], r[6])
        print(r[5])


if __name__ == '__main__':
    main()
