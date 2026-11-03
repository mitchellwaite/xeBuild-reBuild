"""python tools/wip/dehint/iw_ifs.py <file.c> <func> [base.c]

Compile <file.c> and base (default drafts/image_write.c) with -fdump-tree-optimized-details-blocks and print what differs in
<func>'s final gimple: conditionals (operand order = SSA order) and bb frequencies.  Shows when a big assembly diff
is one flipped compare or a frequency change rather than a structural one.  Also the normalised body line diff count."""
import difflib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def dump(src, tag):
    d = os.path.join(iwlib.BUILD, 'a2', 'ifs_' + tag)
    os.makedirs(d, exist_ok=True)
    t = open(src, newline='').read()
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(t)
    subprocess.run([iwlib.GCC, '-c', '-O3', '--param', 'builtin-expect-probability=50', '-I' + os.path.join(iwlib.R, 'src'),
                    '-fdump-tree-optimized-details-blocks', 'a.c', '-o', 'a.o'], cwd=d, capture_output=True)
    f = [x for x in os.listdir(d) if 'optimized' in x][0]
    return open(os.path.join(d, f), errors='replace').read()


def body(t, fn):
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    return m.group(0) if m else ''


src, fn = sys.argv[1:3]
base = sys.argv[3] if len(sys.argv) > 3 else os.path.join(iwlib.R, 'tools/wip/dehint/drafts/image_write.c')
a, b = body(dump(base, 'base'), fn), body(dump(src, 'var'), fn)
fa = re.findall(r'basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', a)
fb = re.findall(r'basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', b)
print('blocks', len(fa), len(fb))
print('freq base', [int(x[2]) for x in fa])
print('freq var ', [int(x[2]) for x in fb])


def ifs(s):
    return [l.strip() for l in s.split('\n') if re.match(r'\s+if \(', l)]


def norm(l):
    return re.sub(r'\.\d+', '', re.sub(r'_\d+', '_N', l))


ia, ib = ifs(a), ifs(b)
print('ifs', len(ia), len(ib))
for x, y in zip(ia, ib):
    if norm(x) != norm(y):
        print('  ', x.ljust(46), y)
