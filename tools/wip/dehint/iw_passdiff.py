"""python tools/wip/dehint/iw_passdiff.py <dirA> <dirB> <func> [-n N]

Both dirs made by iwdump.py with -fdump-tree-all.  For each tree pass in order, normalise the function body (SSA
versions, bb numbers and frequencies stripped) and print how many lines differ, so the first pass where the two
sources differ structurally stands out.  -n N prints the first N differing lines of the first differing passes."""
import difflib, glob, os, re, sys

a, b, fn = sys.argv[1:4]
nshow = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 0


def body(d, name):
    t = open(os.path.join(d, name), errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        return None
    s = m.group(0)
    k = s.find('\n{\n')
    s = s[k:] if k >= 0 else s
    out = []
    for l in s.split('\n'):
        if re.match(r'^  [a-zA-Z].*;$', l) and '=' not in l and 'if' not in l and '(' not in l:
            continue
        l = re.sub(r'\b([A-Za-z_][\w.]*?)_(\d+)\b', r'\1_N', l)
        l = re.sub(r'\b_\d+\b', '_N', l)
        l = re.sub(r'\.\d+', '.N', l)
        l = re.sub(r'\(\d+\)', '(B)', l)
        l = re.sub(r'<bb \d+>', '<bb>', l)
        l = re.sub(r'freq:\d+', 'freq', l)
        l = re.sub(r'bb \d+', 'bb', l)
        l = re.sub(r'\[\d+\.\d+%\]', '', l)
        out.append(l)
    return out


files = sorted(glob.glob(os.path.join(a, 'a.c.*t.*')), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
shown = 0
for f in files:
    n = os.path.basename(f)
    if not os.path.exists(os.path.join(b, n)):
        continue
    x, y = body(a, n), body(b, n)
    if x is None or y is None:
        continue
    d = [l for l in difflib.unified_diff(x, y, lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
    print(n.split('t.', 1)[1].ljust(20), len(d), 'of', len(x))
    if d and nshow and shown < 3:
        shown += 1
        print('\n'.join(d[:nshow]))
