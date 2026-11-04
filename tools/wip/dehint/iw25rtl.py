"""Attempt 25: after iw25trace.py, per RTL pass: does the insn stream of a function differ between the two build dirs, frequencies aside?
python tools/wip/dehint/iw25rtl.py <fn> [dirprefix]: prints each RTL dump as same-insns / DIFF, with the first differing lines of the first DIFF."""
import difflib, os, re, sys
fn = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else 'build/iw/a25/tr'
da, db = out + '_a', out + '_b'
def func(path):
    t = open(path, errors='replace').read()
    m = re.search(r'^;; Function \S+ \(%s,.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m: return None
    r = []
    for l in m.group(0).split('\n'):
        if re.match(r'\s*\(?(insn|jump_insn|call_insn|code_label|note|barrier)', l) or re.match(r'\s+\(', l):
            if 'REG_BR_PROB' in l: continue
            l = re.sub(r'\{[^}]*\}|<[a-z_]+ [0-9a-f]+[^>]*>', '', l)
            l = re.sub(r'\(code_label (\d+) (\d+) (\d+) (\d+ )?\d+ ', r'(code_label    ', l)
            r.append(l)
    return r
names = sorted((x for x in os.listdir(da) if re.match(r'a\.c\.\d+r\.', x)), key=lambda x: int(re.match(r'a\.c\.(\d+)', x).group(1)))
shown = False
for x in names:
    if not os.path.exists(os.path.join(db, x)): continue
    a, b = func(os.path.join(da, x)), func(os.path.join(db, x))
    if a is None or b is None: continue
    st = a == b
    print(x[4:], 'same-insns' if st else 'DIFF', len(a), len(b))
    if not st and not shown:
        shown = True
        for l in list(difflib.unified_diff(a, b, lineterm='', n=1))[:40]:
            print('   ', l[:150])
