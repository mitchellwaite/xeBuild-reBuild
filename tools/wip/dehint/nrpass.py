"""python tools/wip/dehint/nrpass.py <src.c> [out]: for the clone of netRecvVerbose, per GIMPLE pass, the freq of the recv block, of the block holding the recv-fail log, of the tail add (ok path) and of J. Shows which pass moves them."""
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src = os.path.abspath(sys.argv[1])
d = os.path.join(ROOT, 'build', 'nr', 'pass', os.path.basename(os.path.dirname(src)) + '_' + os.path.basename(src)[:-2])
os.makedirs(d, exist_ok=True)
for f in glob.glob(d + '/a.c.*'):
    os.remove(f)
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-I', os.path.join(ROOT, 'src'), '-O3', '-fno-asynchronous-unwind-tables', '-fdump-tree-all-blocks-details', src, '-dumpbase', 'a.c', '-o', 'a.s'], cwd=d, env=env, capture_output=True, stdin=subprocess.DEVNULL)
last = None
for f in sorted(glob.glob(d + '/a.c.*t.*'), key=lambda p: int(re.search(r'\.(\d+)t\.', p).group(1))):
    t = open(f, errors='replace').read()
    i = t.find(';; Function netRecvVerbose.constprop')
    if i < 0:
        continue
    j = t.find('\n;; Function', i + 10)
    s = t[i:j if j > 0 else len(t)]
    out = {}
    for m in re.finditer(r';;\s+basic block (\d+), loop depth \d+, count \d+, freq (\d+)(.*?)(?=;;\s+basic block|\Z)', s, re.S):
        b = m.group(3)
        if ('recv (' in b or 'recvSome' in b or 'RecvSome' in b) and 'hdr' not in b: out['recv'] = m.group(2)
        if re.search(r'got_\d+ = |_\d+ = got_\d+ \+', b) and 'PHI' not in b and 'PHI' not in b: out.setdefault('addgot', []).append(m.group(2))
        if 'could not receive' in b or ('LC' in b and 0): out['R'] = m.group(2)
        if 'select (' in b: out.setdefault('sel', []).append(m.group(2))
        if 'received only' in b: out['log'] = m.group(2)
    l = str(out)
    if l != last:
        print(os.path.basename(f).split('.', 2)[2], l)
        last = l
