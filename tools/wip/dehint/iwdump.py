"""python tools/wip/dehint/iwdump.py <file.c> <outdir> <func> [gcc flags, e.g. -fdump-tree-all]

Compile the draft with the 50 param (IWNP=1: without) and -fdump-rtl-ira -fdump-rtl-peephole2 plus
any extra dumps, and cut each dump down to <func>: <outdir>/<func>.<suffix>."""
import glob, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

src, out, fn = sys.argv[1:4]
extra = sys.argv[4:]
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, 'a.c*')):
    os.remove(f)
shutil.copy(src, os.path.join(out, 'a.c'))
flags = [] if os.environ.get('IWNP') else ['--param', 'builtin-expect-probability=50']
r = subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'),
                    '-fdump-rtl-ira', '-fdump-rtl-peephole2', '-fdump-rtl-expand'] + extra + ['a.c', '-o', 'a.o'],
                   cwd=out, capture_output=True, text=True)
print(r.stderr[:500])
for f in glob.glob(os.path.join(out, 'a.c.*')):
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if m:
        suf = f.split('a.c.')[1]
        suf = re.sub(r'^\d+[tri]\.', '', suf)
        open(os.path.join(out, fn + '.' + suf), 'w', newline='\n').write(m.group(0))
print(sorted(x for x in os.listdir(out) if x.startswith(fn)))
