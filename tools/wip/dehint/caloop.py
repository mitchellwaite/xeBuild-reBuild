"""Print the assembly of sendAvatarData's send loop, from the `sending %03d` setup backwards a bit.

python tools/wip/dehint/caloop.py <file.c> [flags]
Prints the lines from the 'sending %d items' log call to the netSendFile call of the loop.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-O3', '-I', os.path.join(ROOT, 'src'),
                    '-fno-asynchronous-unwind-tables'] + sys.argv[2:] + [sys.argv[1], '-o', '-'],
                   env=env, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr)
t = r.stdout.split('\n')
s = t.index('_sendAvatarData:')
fn = t[s:]
for i, l in enumerate(fn):
    if l == '\t.def\t_sendDir;' or l.startswith('_sendDir:'):
        fn = fn[:i]
        break
calls = [i for i, l in enumerate(fn) if '_netSendFile' in l]
start = max(0, calls[0] - 30)
print('\n'.join(l for l in fn[start:calls[0] + 8]))
