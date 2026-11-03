"""python tools/wip/dehint/iwpasses.py <a.c> <b.c> <func> [-n N]: compile both with every tree dump, cut each
to <func>, and list passes (in order) where the two differ, with the size of the difference.  Prints the
diff at the first N differing passes (default 1).  IWNP=1: no 50 param. A_FLAGS / B_FLAGS env: extra flags."""
import difflib, glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

a, b, fn = sys.argv[1:4]
n = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 1
flags = [] if os.environ.get('IWNP') else ['--param', 'builtin-expect-probability=50']


def run(src, d, extra):
    d = os.path.join(iwlib.BUILD, d)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    t = open(src, newline='').read().replace('\r\n', '\n')
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(t)
    subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + extra + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-all',
                    'a.c', '-o', 'a.o'], cwd=d, capture_output=True)
    res = {}
    for f in glob.glob(os.path.join(d, 'a.c.*')):
        name = f.split('a.c.')[1]
        s = open(f, errors='replace').read()
        m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), s, re.S | re.M)
        if m:
            res[name] = re.sub(r'decl_uid=\d+|cgraph_uid=\d+|symbol_order=\d+|funcdef_no=\d+', '', m.group(0))
    return res


ra = run(a, 'pa', os.environ.get('A_FLAGS', '').split())
rb = run(b, 'pb', os.environ.get('B_FLAGS', '').split())
shown = 0
for k in sorted(set(ra) & set(rb), key=lambda x: int(re.match(r'(\d+)', x).group(1))):
    if ra[k] != rb[k]:
        la, lb = ra[k].split('\n'), rb[k].split('\n')
        d = [l for l in difflib.unified_diff(la, lb, lineterm='', n=1)]
        print('%-22s differs: %d lines' % (k, sum(1 for l in d if l[:1] in '+-')))
        if shown < n:
            print('\n'.join(x[:130] for x in d[:80]))
            shown += 1
