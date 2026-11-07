"""Attempt 50: loadBl24's own profile per body (a50_bl24.py's BODIES): the summed frequency of its
defaultBl60 call blocks at profile_estimate (of 10000).  loadBl24 is late-inlined, so this share is
what IPA scales into both loaders' case 24 (console's r = 1 block = share x its call block x 10.1%).
python tools/wip/dehint/bdgen/a50_bl24share.py"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a50_bl24 as B

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
src = open(B.BASE, newline='').read()
for name, body in B.BODIES.items():
    if name in ('sz', 'r6'):
        continue
    t = src.replace(B.OLD, body)
    d = tempfile.mkdtemp(dir=os.path.join(R, 'build', 'bd', 'a50'))
    open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + t)
    subprocess.run([GCC, '-c', '-O3', '--param', 'builtin-expect-probability=99', '-I' + os.path.join(R, 'src'),
                    'b.c', '-o', 'b.o', '-fdump-tree-profile_estimate-details-blocks'], cwd=d, env=env, check=True)
    dump = [f for f in os.listdir(d) if f.endswith('profile_estimate')][0]
    x = open(os.path.join(d, dump), errors='replace').read()
    parts = [m.start() for m in re.finditer(r'^;; Function loadBl24 ', x, re.M)]
    body_txt = x[parts[-1]:x.find('\n;; Function ', parts[-1] + 10)]
    tot = 0
    for m in re.finditer(r';;   basic block \d+, loop depth \d+, count \d+, freq (\d+).*?\n(.*?)(?=;;   basic block|\Z)', body_txt, re.S):
        if 'defaultBl60' in m.group(2):
            tot += int(m.group(1))
    print('%-6s calls %5d' % (name, tot))
