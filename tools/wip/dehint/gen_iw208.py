# attempt 13: near13 (w2) with the attribute's one flag swapped for any other optimizer flag gcc lists: the attribute still counts as one trick, so a hit is lnp2 + dead test gone.
import os, re, subprocess
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
ATTR = 'optimize("no-tree-scev-cprop")'
out = subprocess.run([os.path.join('tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe'), '-Q', '-O3', '--help=optimizers'], capture_output=True, text=True,
                     env=dict(os.environ, PATH=os.path.abspath(os.path.join('tools', 'toolchain-4745', 'mingw32', 'bin')) + os.pathsep + os.environ['PATH'])).stdout
A = []
for l in out.split('\n'):
    m = re.match(r'\s+-f([a-z0-9-]+)\s+\[(enabled|disabled)\]', l)
    if m:
        name, st = m.groups()
        f = ('no-' + name) if st == 'enabled' else name
        A.append((f, [(ATTR, 'optimize("%s")' % f)]))
AXES = [A]
FLAGS = []
