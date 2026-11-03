"""python tools/wip/dehint/wbdump.py <src.c> [fn]: dumps for one net function.

Compiles to build/wb/tr/<basename>/a.c-style dumps and prints: profile_estimate
predictions, the optimized GIMPLE, block freqs at bbro and the trace log, and
jump2's crossjump lines.  WB_FN or argv[2] picks the function (default netWriteBlocks).
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src = os.path.abspath(sys.argv[1])
fn = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('WB_FN', 'netWriteBlocks')
d = os.path.join(ROOT, 'build', 'wb', 'tr', os.path.splitext(os.path.basename(src))[0])
os.makedirs(d, exist_ok=True)
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
extra = os.environ.get('WB_FLAGS', '').split()
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3',
                '-I', os.path.join(ROOT, 'src'), '-fdump-tree-profile_estimate-details', '-fdump-tree-optimized-all',
                '-fdump-rtl-jump2-details', '-fdump-rtl-bbro-details', '-fdump-tree-einline-details'] + extra + [src, '-o', 'a.s'],
               cwd=d, env=env, check=True)


def section(pat):
    f = next(x for x in os.listdir(d) if re.search(pat, x))
    t = open(os.path.join(d, f)).read()
    m = re.search(r';; Function %s \(' % fn, t)
    if not m:
        return ''
    s = t[m.start():]
    j = s.find('\n;; Function ', 10)
    return s[:j] if j > 0 else s


what = os.environ.get('WB_SHOW', 'pe,opt,bb,cj')
if 'pe' in what:
    print('=== profile_estimate')
    for l in section(r'profile_estimate$').split('\n'):
        if re.match(r'(Predictions for bb|  [a-zA-Z ]+heuristics|  (first match|combined|DS theory|negative|opcode|call|early|pointer|loop|const|null|goto|continue|noreturn|guessed|hot|cold))', l):
            print(l)
if 'opt' in what:
    print('=== optimized')
    print(section(r'optimized$'))
if 'bb' in what:
    print('=== bbro')
    s = section(r'r\.bbro$')
    k = s.find('Reordering with the STC')
    if k >= 0:
        for m in re.finditer(r'^;; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', s[:k], re.M):
            print('bb', m.group(1), 'f', m.group(3))
        print('\n'.join(l for l in s[k:].split('\n') if re.match(r'(STC|Getting bb|Basic block|Trace |Connection|Duplicated|  *[0-9]+ )', l))[:5000])
if 'cj' in what:
    print('=== jump2')
    for l in section(r'r\.jump2$').split('\n'):
        if re.search(r'[Cc]ross|merg|head|Forward', l):
            print(l)
