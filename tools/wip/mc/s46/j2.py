"""j2.py SRC.c TAG: plain compile with jump2 dump; print crossjump lines of mode_client."""
import os, subprocess, sys, re
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FL = ['-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions', '--param', 'builtin-expect-probability=50']
src, tag = sys.argv[1], sys.argv[2]
sd = os.path.join(ROOT, 'build', 'v', 'mc46', 'j_' + tag); os.makedirs(sd, exist_ok=True)
open(os.path.join(sd, 'm.c'), 'w', newline='\n').write(open(src).read())
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-fno-asynchronous-unwind-tables'] + FL + ['-I' + os.path.join(ROOT, 'src'), '-fdump-rtl-jump2-details', 'm.c', '-o', 'm.s'], cwd=sd, env=env, capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr)
d = [f for f in os.listdir(sd) if 'jump2' in f][0]
t = open(os.path.join(sd, d)).read(); a = t.find(';; Function mode_client'); b = t.find('\n;; Function', a + 10); t = t[a:b if b > 0 else None]
for l in t.split('\n'):
    if 'Cross jumping' in l or 'Splitting' in l: print(l)
