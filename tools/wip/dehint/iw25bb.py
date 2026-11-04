"""Attempt 25: after iw25trace.py, diff bb-reorder's trace log (freqs, keys, connections) and RA of a function between the two build dirs.
python tools/wip/dehint/iw25bb.py <fn> [max lines] [dirprefix]"""
import difflib, re, sys
fn = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 80
out = sys.argv[3] if len(sys.argv) > 3 else 'build/iw/a25/tr'
def f(d):
    t = open(d + '/a.c.274r.bbro', errors='replace').read()
    m = re.search(r'^;; Function \S+ \(%s,.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M).group(0)
    h = m[:m.find('(note')]
    return [re.sub(r'\s+', ' ', l) for l in h.split('\n')]
a, b = f(out + '_a'), f(out + '_b')
for l in list(difflib.unified_diff(a, b, lineterm='', n=0))[:mx]:
    print(l[:170])
