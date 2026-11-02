"""python tools/wip/dehint/iradump.py <file.c> [gcc flags]: readFileIn's IRA colouring, named.

Prints each allocno's pseudo with the variable name gcc gives it, its total cost,
frequency, thread, and the register assigned, in pop order.
"""
import os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src = os.path.abspath(sys.argv[1])
d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'rf'))
shutil.copy(src, os.path.join(d, 'a.c'))
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
flags = sys.argv[2:] or ['-O3']
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-I', os.path.join(ROOT, 'src'), '-fno-asynchronous-unwind-tables',
                '-fdump-rtl-ira', '-fdump-rtl-expand'] + flags + ['a.c'], cwd=d, env=env, check=True)
f = next(x for x in os.listdir(d) if x.endswith('r.ira'))
t = open(os.path.join(d, f)).read()
t = t[t.index(';; Function readFileIn '):]
t = t[:t.index(';; Function calcConfigSum')]
names = {}
for m in re.finditer(r'\(reg(?:/\w+)*:\w+ (\d+)(?: \[ ([^\]]*) \])?', t):
    if m.group(2):
        names.setdefault(m.group(1), m.group(2).strip())
print('\n'.join(l for l in t.split('\n') if 'Forming thread' in l or 'Result (freq' in l))
info = {}
for m in re.finditer(r'a(\d+)\(r(\d+),l0\) costs:.*?MEM:(-?\d+)', t):
    info[m.group(2)] = m.group(3)
for m in re.finditer(r'Popping a(\d+)\(r(\d+),l0\)\s+--\s+(.*)', t):
    print('r%-4s %-18s mem=%-7s %s' % (m.group(2), names.get(m.group(2), '?'), info.get(m.group(2)), m.group(3)))
for m in re.finditer(r'^ *a(\d+)\(r(\d+),l0\).*', t, re.M):
    pass
shutil.rmtree(d)
