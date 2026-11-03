"""python tools/wip/dehint/nrrtl.py <src.c> [regex]: dump the clone through expand/fwprop/cse/ira, print its GIMPLE lines and each
RTL pass's insns matching regex (default got|want|n); then got's MEM and class from the IRA dump. Dumps to build/nr/rtl/<name>."""
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src = os.path.abspath(sys.argv[1])
rx = sys.argv[2] if len(sys.argv) > 2 else r'got'
d = os.path.join(ROOT, 'build', 'nr', 'rtl', os.path.basename(os.path.dirname(src)) + '_' + os.path.basename(src)[:-2])
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(src).read())
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-I', os.path.join(ROOT, 'src'), '-fno-asynchronous-unwind-tables', '-O3',
                '-fdump-tree-optimized-blocks', '-fdump-rtl-expand', '-fdump-rtl-fwprop1', '-fdump-rtl-cprop1', '-fdump-rtl-cse1', '-fdump-rtl-ira', 'a.c', '-o', 'a.s'],
               cwd=d, env=env, check=True, stdin=subprocess.DEVNULL)


def clone(pat):
    t = open(glob.glob(os.path.join(d, pat))[0]).read()
    i = t.index(';; Function netRecvVerbose.constprop')
    j = t.find('\n;; Function', i + 10)
    return t[i:j if j > 0 else len(t)]


for l in clone('*optimized').split('\n'):
    if re.search(rx, l) or 'recv' in l:
        print(l)
for p in ('*expand', '*fwprop1', '*r.ira'):
    s = clone(p)
    if 'ira' in p:
        s = s[s.find('Disposition'):]
    print('--', p)
    for m in re.finditer(r'^\((insn|jump_insn) .*?(?=^\(|^;;|\Z)', s, re.M | re.S):
        x = re.sub(r'\s+', ' ', m.group(0))
        if re.search(rx, x):
            print(x[:170])
s = clone('*r.ira')
last = {}
for m in re.finditer(r'a(\d+)\(r(\d+),l0\) costs:(.*?)MEM:(-?\d+),(-?\d+)', s):
    g = re.search(r'GENERAL_REGS:(-?\d+),(-?\d+)', m.group(3))
    last[m.group(2)] = (m.group(5), g.group(2) if g else '?')
for m in re.finditer(r'Popping a(\d+)\(r(\d+),l0\)\s+--\s+(.*)', s):
    if m.group(2) in last and int(last[m.group(2)][0]) > 1000:
        print('r%s MEM %s class %s -> %s' % (m.group(2), last[m.group(2)][0], last[m.group(2)][1], m.group(3)))
