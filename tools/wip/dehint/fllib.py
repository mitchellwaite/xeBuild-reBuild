"""fllib: compile variants of filelist_ini.c as build.sh does and compare them.

FLBASE=<file> sets the base source (default src/filelist_ini.c).  build/filelist_ini/reference.o holds a matching
build's filelist_ini.o.

compile(src, flags, tag)  -> object path under build/filelist_ini/v/
same(o)                   -> whole-object byte match
sections(o)               -> {section: bytes}; secdiff(o) lists the differing ones
fndiff(o)                 -> {function: differing instruction lines}, targets
                             function-relative so layout shows up
sub(src, old, new)        -> replace exactly one occurrence, or raise
sweep(vars, flags)        -> compile {name: src} in parallel, print sorted scores
python fllib.py <file> [flags..] scores one file; DIFF=<fn> prints that diff.
"""
import difflib, os, re, shutil, struct, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
GCC = os.path.join(TC, 'gcc.exe')
OBJDUMP = os.path.join(TC, 'objdump.exe')
BD = os.path.join(R, 'build', 'filelist_ini')
OUT = os.path.join(BD, 'v')
REF = os.path.join(BD, 'reference.o')
DRAFT = os.path.join(R, 'tools', 'wip', 'dehint', 'drafts', 'filelist_ini_final.c')
SRC = os.environ.get('FLBASE') or os.path.join(R, 'src', 'filelist_ini.c')
ALLFLAGS = ['-O3', '-fno-tree-loop-vectorize', '--param', 'builtin-expect-probability=65',
            '--param', 'lra-inheritance-ebb-probability-cutoff=60']
FLAGS = list(ALLFLAGS)
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(REF):
    shutil.copy(os.path.join(R, 'build', 'obj', 'filelist_ini.o'), REF)


def base():
    return open(SRC, newline='').read()


def sub(src, old, new, count=1):
    if src.count(old) != count:
        raise ValueError('%d occurrences of %r' % (src.count(old), old[:60]))
    return src.replace(old, new)


def compile(src, flags=None, tag='t'):
    o = os.path.join(OUT, tag + '.o')
    if os.path.exists(o):
        os.remove(o)
    inp = ('#line 1 "filelist_ini.c"\n' + src).encode()
    fl = list(FLAGS if flags is None else flags)
    p = subprocess.run([GCC, '-c'] + fl + ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=OUT)
    if p.returncode or not os.path.exists(o):
        sys.stderr.write(tag + ': ' + p.stderr.decode(errors='replace')[:1500] + '\n')
        return None
    return o


def same(o):
    return o is not None and open(o, 'rb').read() == open(REF, 'rb').read()


def sections(o):
    """{name: raw bytes} from the COFF section table."""
    b = open(o, 'rb').read()
    nsec = struct.unpack_from('<H', b, 2)[0]
    optsz = struct.unpack_from('<H', b, 16)[0]
    r = {}
    for i in range(nsec):
        h = 20 + optsz + 40 * i
        name = b[h:h + 8].rstrip(b'\0').decode()
        size, ptr = struct.unpack_from('<II', b, h + 16)
        r[name] = b[ptr:ptr + size] if ptr else bytes(size)
    return r


def secdiff(o):
    a, b = sections(REF), sections(o)
    return [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]


def dis(o):
    t = subprocess.run([OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       stdout=subprocess.PIPE).stdout.decode(errors='replace')
    fns, cur, start = {}, None, 0
    for ln in t.splitlines():
        m = re.match(r'^([0-9a-f]+) <(.+)>:', ln)
        if m:
            cur = m.group(2)
            start = int(m.group(1), 16)
            fns[cur] = []
            continue
        if cur is None or not ln.strip():
            continue
        m = re.match(r'\s*([0-9a-f]+):\s*(.*)', ln)
        if m:
            s = m.group(2).strip()
            s = re.sub(r'\b([0-9a-f]+) <[^>]*>', lambda k: '.%x' % (int(k.group(1), 16) - start), s)
            fns[cur].append(s)
        else:
            fns[cur].append(re.sub(r'^\s*[0-9a-f]+:', '', ln).strip())
    return fns


_ref = {}


def fndiff(o):
    if not _ref:
        _ref.update(dis(REF))
    d = dis(o)
    r = {}
    for k, v in _ref.items():
        w = d.get(k, [])
        if v != w:
            r[k.lstrip('_')] = sum(1 for x in difflib.ndiff(v, w) if x[0] in '+-')
    return r


def score(o):
    if o is None:
        return (10**7, 'gcc failed', {}, [])
    if same(o):
        return (0, 'MATCH', {}, [])
    fd = fndiff(o)
    sd = secdiff(o)
    # a variant that differs only in data still scores above a match
    return (sum(fd.values()) + 0.5 * bool(sd), 'differ', fd, sd)


def sweep(vs, flags=None, prefix='s', workers=4, show=30):
    """vs: {name: src} or {name: (src, flags)}."""
    def one(kv):
        n, v = kv
        s, fl = v if isinstance(v, tuple) else (v, flags)
        tag = prefix + '_' + re.sub(r'\W', '_', n)
        return (n, score(compile(s, fl, tag)))
    with ThreadPoolExecutor(workers) as ex:
        rs = list(ex.map(one, vs.items()))
    rs.sort(key=lambda x: x[1][0])
    for n, (sc, st, fd, sd) in rs[:show]:
        print('%8s %-28s %s sec=%s' % (sc, n, fd, sd))
    return rs


if __name__ == '__main__':
    f = sys.argv[1]
    fl = sys.argv[2:] or None
    o = compile(open(f, newline='').read(), fl, 'one')
    sc = score(o)
    print(sc[1], sc[2], sc[3])
    fn = os.environ.get('DIFF')
    if fn:
        for ln in difflib.unified_diff(dis(REF)['_' + fn], dis(o)['_' + fn], lineterm='', n=2):
            print(ln)
