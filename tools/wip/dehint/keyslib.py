"""keyslib: compile variants of keys.c exactly as build.sh does and compare them.

compile(src, flags, tag) -> path of the .o under build/keys/v/
same(path)               -> whole-object byte match against build/keys/reference.o
fndiff(path)             -> {function: number of differing instruction lines}
                            (objdump without addresses; jump targets normalised to
                            function-relative offsets so layout shows up)
FLAGS is build.sh's current keys flags.  python keyslib.py <file> [flags..] prints
the score of one file.
"""
import difflib, os, re, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
GCC = os.path.join(TC, 'gcc.exe')
OBJDUMP = os.path.join(TC, 'objdump.exe')
OUT = os.path.join(R, 'build', 'keys', 'v')
REF = os.path.join(R, 'build', 'keys', 'reference.o')
SRC = os.environ.get('KEYSBASE') or os.path.join(R, 'src', 'keys.c')
FLAGS = ['-O3', '--param', 'builtin-expect-probability=60']
os.makedirs(OUT, exist_ok=True)


def base():
    return open(SRC, newline='').read()


def compile(src, flags=None, tag='t', extra=()):
    """returns the object path, or None if gcc failed."""
    o = os.path.join(OUT, tag + '.o')
    if os.path.exists(o):
        os.remove(o)
    inp = ('#line 1 "keys.c"\n' + src).encode()
    fl = list(FLAGS if flags is None else flags) + list(extra)
    p = subprocess.run([GCC, '-c'] + fl + ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=OUT)
    if p.returncode or not os.path.exists(o):
        sys.stderr.write(p.stderr.decode(errors='replace')[:2000])
        return None
    return o


def same(o):
    return o is not None and open(o, 'rb').read() == open(REF, 'rb').read()


_refcache = {}


def dis(o):
    """{fn: [lines]} from objdump -d -r, addresses dropped, branch targets made relative."""
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
            s = ln.strip()
            fns[cur].append(s)
    return fns


def fndiff(o, ref=None):
    if not _refcache:
        _refcache.update(dis(REF))
    d = dis(o)
    r = {}
    for k, v in _refcache.items():
        w = d.get(k, [])
        if v != w:
            n = sum(1 for x in difflib.ndiff(v, w) if x[0] in '+-')
            r[k] = n
    return r


if __name__ == '__main__':
    f = sys.argv[1]
    fl = sys.argv[2:] or None
    o = compile(open(f, newline='').read(), fl, 'one')
    print('MATCH' if same(o) else 'differ', fndiff(o))
