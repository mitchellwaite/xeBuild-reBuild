"""python tools/wip/dehint/bdopt.py file.c fn regex [regex..]: the blocks of fn's .optimized dump
holding a line that matches a regex, with their frequencies.  The dump stays in build/bd/optdump
(overwritten by the next run)."""
import glob, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
d = os.path.join(R, 'build', 'bd', 'optdump')
os.makedirs(d, exist_ok=True)
src = '#line 1 "build.c"\n' + open(sys.argv[1], newline='').read()
subprocess.run([os.path.join(TC, 'gcc.exe'), '-c', '-O3', '--param', 'builtin-expect-probability=98', '-I' + os.path.join(R, 'src'),
                '-fdump-tree-optimized-blocks-details','-x', 'c', '-', '-o', 'o.o'], input=src.encode(), cwd=d, check=True)
f = glob.glob(os.path.join(d, '*.optimized'))[0]
p = False
bb = ''
pats = [re.compile(x) for x in sys.argv[3:]]
for l in open(f, errors='replace'):
    if l.startswith(';; Function '):
        p = l.split()[2] == sys.argv[2]
    elif p:
        m = re.search(r'basic block (\d+), loop depth \d+, count \d+, freq (\d+)', l)
        if m:
            bb = 'bb %s [%s]' % m.groups()
        elif any(x.search(l) for x in pats):
            print(bb, l.strip()[:100])
