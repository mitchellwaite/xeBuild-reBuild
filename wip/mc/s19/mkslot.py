"""mkslot.py VARIANT.c SLOTDIR: plain compile (build.sh's mode_client flags, no profile) of
VARIANT.c into an s18-style slot dir (m.c.274r.bbro, m.c.267r.compgotos, fdo.s), so
wip/mc/s18/analyze.py, hsim.py and hanneal.py can replay its real bb-reorder history."""
import os, shutil, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FLAGS = ['-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions',
         '--param', 'builtin-expect-probability=50']
src, sd = sys.argv[1], sys.argv[2]
os.makedirs(sd, exist_ok=True)
shutil.copy(src, os.path.join(sd, 'm.c'))
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables']
                   + FLAGS + ['-I' + os.path.join(ROOT, 'src'), '-fdump-rtl-bbro-details',
                              '-fdump-rtl-compgotos-blocks', 'm.c', '-o', 'fdo.s'],
                   cwd=sd, env=env, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr)
print(sd)
