"""python tools/wip/dehint/nrgrep.py <dumpdir> <suffix> <fnprefix> <regex> [ctx]: lines of one function's dump."""
import os, re, sys
d, suf, fn, rx = sys.argv[1:5]
ctx = int(sys.argv[5]) if len(sys.argv) > 5 else 0
f = next(x for x in os.listdir(d) if x.endswith(suf))
t = open(os.path.join(d, f)).read()
i = t.index(';; Function ' + fn)
s = t[i:]
j = s.find('\n;; Function ', 10)
s = (s[:j] if j > 0 else s).split('\n')
out = set()
for n, l in enumerate(s):
    if re.search(rx, l):
        out.update(range(max(0, n - ctx), min(len(s), n + ctx + 1)))
for n in sorted(out):
    print(s[n][:220])
