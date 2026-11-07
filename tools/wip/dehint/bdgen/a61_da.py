"""Attempt 61: one function's -dA assembly (block numbers, frequencies, edges) for a variant, p99.
python tools/wip/dehint/bdgen/a61_da.py <variant.c> <function> [out.s] [-p N]"""
import os, re, subprocess, sys, tempfile
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
OUT = os.path.join(R, 'build', 'bd', 'a61', 'da')
os.makedirs(OUT, exist_ok=True)
a = sys.argv[1:]
p = 99
if '-p' in a:
    i = a.index('-p'); p = int(a[i + 1]); del a[i:i + 2]
d = tempfile.mkdtemp(dir=OUT)
open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + open(a[0], newline='').read())
fl = ['--param', 'builtin-expect-probability=%d' % p] if p else []
subprocess.run([GCC, '-S', '-dA', '-O3'] + fl + ['-I' + os.path.join(R, 'src'), 'b.c', '-o', 'b.s'], cwd=d, env=env, check=True)
s = open(os.path.join(d, 'b.s')).read()
m = re.search(r'^_%s:\n(.*?)\n\t\.cfi_endproc' % re.escape(a[1]), s, re.S | re.M)
t = m.group(1)
if len(a) > 2:
    open(a[2], 'w', newline='\n').write(t)
else:
    print(t)
