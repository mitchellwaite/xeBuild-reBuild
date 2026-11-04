"""python tools/wip/dehint/iw13cmp.py <file.c> [fn] [pass] : every `if (a != b)`-style test of fn in the given tree dump (default
writeFsTable, optimized), with block number; for reading compare operand orders against src. Writes the dump dir under build/iw/a13/cmp_<name>."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
path = sys.argv[1]
fn = sys.argv[2] if len(sys.argv) > 2 else 'writeFsTable'
ps = sys.argv[3] if len(sys.argv) > 3 else 'optimized'
name = os.path.splitext(os.path.basename(path))[0]
d = os.path.join(iwlib.BUILD, 'a13', 'cmp_' + name)
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-all-blocks', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
f = glob.glob(os.path.join(d, 'a.c.*' + ps))[0]
t = open(f, errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M).group(0)
bb = None
for l in m.split('\n'):
    k = re.search(r'basic block (\d+)', l) or re.match(r'\s*<bb (\d+)>', l)
    if k:
        bb = k.group(1)
    if re.match(r'\s+if \(', l):
        print('bb%s %s' % (bb, l.strip()))
