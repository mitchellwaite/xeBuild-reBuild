"""Attempt 25: first pass where one function's dump differs between two sources.
python tools/wip/dehint/iw25trace.py <fn asm name part, e.g. imgAdd.constprop.1> <a.c[:N]> <b.c[:N]> [outdir]
Compiles both with all tree and rtl dumps (N = builtin-expect-probability), then for each dump in pass order extracts the
function and compares it with SSA numbers, uids and frequencies kept in one mode and removed in the other.
Prints, per pass, `same`, `freq-only` (identical once freq/count/prob numbers are dropped) or `DIFF`."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def build(spec, d):
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    p, _, n = spec.partition(':')
    text = open(p, newline='').read().replace('\r\n', '\n')
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(text)
    fl = ['--param', 'builtin-expect-probability=' + n] if n else []
    subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), 'a.c', '-o', 'a.o', '-fdump-tree-all-blocks-details', '-fdump-rtl-all-blocks-details', '-fdump-ipa-all-details'] + fl, cwd=d, check=True)


def func(path, fn):
    t = open(path, errors='replace').read()
    m = re.search(r'^;; Function \S+ \(%s,.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    return m.group(0) if m else None


def nofreq(s):
    s = re.sub(r'\bfreq(?:uency)?[ :=]*\d+', 'freq', s)
    s = re.sub(r'\bcount[ :=]*\d+', 'count', s)
    s = re.sub(r'\bprob[a-z]*[ :=]*[\d.]+%?', 'prob', s)
    s = re.sub(r'\[[\d.]+%\]', '[p]', s)
    s = re.sub(r'\d+\.\d+%', 'p%', s)
    s = re.sub(r'REG_BR_PROB \d+', 'REG_BR_PROB', s)
    return s


fn, a, b = sys.argv[1:4]
out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(iwlib.BUILD, 'a25', 'tr')
da, db = out + '_a', out + '_b'
build(a, da)
build(b, db)
names = sorted(x for x in os.listdir(da) if re.match(r'a\.c\.\d+[tri]\.', x))
names.sort(key=lambda x: int(re.match(r'a\.c\.(\d+)', x).group(1)))
for x in names:
    if not os.path.exists(os.path.join(db, x)):
        continue
    fa, fb = func(os.path.join(da, x), fn), func(os.path.join(db, x), fn)
    if fa is None or fb is None:
        continue
    st = 'same' if fa == fb else ('freq-only' if nofreq(fa) == nofreq(fb) else 'DIFF')
    print(x[4:], st)
