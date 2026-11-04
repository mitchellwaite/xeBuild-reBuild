"""python tools/wip/dehint/iw14names.py <file.c> [fn] [-p passsubstr] : per tree pass, the SSA names of fn that appear (new) and disappear
against the previous pass, in the order they first occur in the dump. For reading the free-name stack (which names ivopts gets).
Dumps go to build/iw/a14/nm_<name>."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
a = sys.argv[1:]
only = None
if '-p' in a:
    i = a.index('-p'); only = a[i + 1]; del a[i:i + 2]
path = a[0]
fn = a[1] if len(a) > 1 else 'writeFsTable'
name = os.path.splitext(os.path.basename(path))[0]
d = os.path.join(iwlib.BUILD, 'a14', 'nm_' + name)
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-all', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
fs = glob.glob(os.path.join(d, 'a.c.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
rx = re.compile(r'(?<![\w.])(?:[A-Za-z_][\w.]*)?_(\d+)(?:\(D\))?\b')
for f in fs:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    body = m.group(0)
    k = body.find('\n{')
    if k < 0: continue
    body = body[k:]
    order = []
    seen = {}
    for x in re.finditer(r'(?<![\w.])((?:[A-Za-z_][\w.]*)?_(\d+))(?:\(D\))?\b', body):
        n = int(x.group(2))
        if n not in seen:
            seen[n] = x.group(1); order.append(n)
    if prev is not None:
        new = [n for n in order if n not in prev]
        gone = sorted(n for n in prev if n not in seen)
        p = re.search(r'\.\d+t\.(.*)$', f).group(0)
        if (new or gone) and (not only or only in p):
            print(p, 'new', len(new), [seen[n] for n in new] if only else new, 'gone', len(gone), gone)
    prev = seen
