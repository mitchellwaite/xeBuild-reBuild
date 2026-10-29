"""pre-bbro CFG (trace numbering) of a slot: python dumpcfg.py SLOT > out"""
import os, subprocess, sys, glob
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'; sys.path.insert(0, ROOT + r'\tools\wip'); import mcfdo
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
F1 = ROOT + r'\build\mcsp'; sd = F1 + '\slot' + sys.argv[1]
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
d = sd + r'\cfgd'; os.makedirs(d, exist_ok=True)
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables'] + mcfdo.FL + ['-fbranch-probabilities', '-fprofile-dir=' + sd, '-fdump-rtl-compgotos-blocks-details', os.path.join(F1, 'm.c'), '-o', '-'], cwd=sd, env=env, capture_output=True, text=True)
f = os.path.join(sd, 'm.c.267r.compgotos')
print(subprocess.run([sys.executable, ROOT + r'\tools\wip\mc\cfgdump.py', f, 'mode_client'], capture_output=True, text=True).stdout)
