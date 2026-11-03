"""python tools/wip/dehint/nsira.py <src.c> [gcc flags]: netSendFile's IRA view of the params.

Prints each pseudo named after buf/name/len with its MEM cost and class choice, and the insns using buf.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src = os.path.abspath(sys.argv[1])
extra = sys.argv[2:]
d = os.path.join(ROOT, 'build', 'ns', 'ira', os.path.splitext(os.path.basename(src))[0])
os.makedirs(d, exist_ok=True)
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3',
                '-I', os.path.join(ROOT, 'src'), '-fdump-rtl-ira'] + extra + [src, '-o', 'a.s'],
               cwd=d, env=env, check=True)
f = next(x for x in os.listdir(d) if x.endswith('r.ira'))
t = open(os.path.join(d, f)).read()
t = t[t.index(';; Function netSendFile ('):]
j = t.find('\n;; Function ', 10)
t = t[:j] if j > 0 else t
regs = set(re.findall(r'\(reg/?\S*:SI (\d+) \[ (?:buf|name|len)', t))
print('regs', sorted(regs))
seen = set()
for r in sorted(regs):
    for m in re.finditer(r'a\d+\(r%s,l\d\) costs:.*' % r, t):
        l = m.group(0)
        c = re.search(r'GENERAL_REGS:(-?\d+),(-?\d+) MEM:(-?\d+),(-?\d+)', l)
        print(' ', l.split(' ')[0], c.groups() if c else l[-40:])
    for m in re.finditer(r'a\d+ \(r%s,l\d\) best \S+, allocno \S+' % r, t):
        print(' ', m.group(0))
# the insns of buf's pseudo in the final RTL with block freq
b = 0
fin = t[t.rfind('\n;; basic block 2,') if t.rfind('\n;; basic block 2,') > 0 else 0:]
cur = None
for l in fin.split('\n'):
    m = re.match(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', l)
    if m:
        cur = m.groups()
    if re.search(r'\[ (buf)\S* \]|\[\d+ (buf)\+0', l):
        print('  bb', cur, l.strip()[:110])
m = re.search(r'Disposition:\n(.*?)\n\n', t, re.S)
if m:
    print(m.group(1)[:700])
