"""Compare a net draft's object with build/obj/net.o from the last matching build.

python tools/wip/dehint/nrobj.py <file.c>...
Plain -O3.  Compares .text disassembly, .rdata and .data contents, prints counts and the first differences.
"""
import concurrent.futures as cf, difflib, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
OD = os.path.join(BIN, 'objdump.exe')
REF = os.path.join(ROOT, 'build', 'obj', 'net.o')


def dump(o):
    a = subprocess.run([OD, '-d', '--no-show-raw-insn', '-r', '-M', 'intel', '-j', '.text', o], env=env, capture_output=True, text=True).stdout
    b = subprocess.run([OD, '-s', '-j', '.rdata', '-j', '.data', o], env=env, capture_output=True, text=True).stdout
    return (a.split('\n')[3:], b.split('\n')[3:])


def one(path):
    os.makedirs(os.path.join(ROOT, 'build', 'nr'), exist_ok=True)
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'nr'))
    try:
        shutil.copy(path, os.path.join(d, 'net.c'))
        r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-O3', '-I', os.path.join(ROOT, 'src'), '-fno-asynchronous-unwind-tables',
                            'net.c', '-o', 'x.o'], cwd=d, env=env, capture_output=True, text=True)
        if r.returncode:
            return path, 'ERROR ' + r.stderr[:300]
        ta, da = dump(REF)
        tb, db = dump(os.path.join(d, 'x.o'))
        dt = [l for l in difflib.unified_diff(ta, tb, lineterm='', n=0) if l[0] in '+-' and l[:3] not in ('+++', '---')]
        dd = [l for l in difflib.unified_diff(da, db, lineterm='', n=0) if l[0] in '+-' and l[:3] not in ('+++', '---')]
        return path, 'text %d data %d\n%s' % (len(dt), len(dd), '\n'.join((dt + dd)[:40]))
    finally:
        shutil.rmtree(d, ignore_errors=True)


with cf.ThreadPoolExecutor(4) as ex:
    for p, r in ex.map(one, sys.argv[1:]):
        print(os.path.basename(p), r)
