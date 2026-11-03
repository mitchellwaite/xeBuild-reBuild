"""After casweep.py: run caobj.py's section compare on a generator's variants with at most N fncmp lines.

python tools/wip/dehint/caobjbest.py <gen name> [N]   (default 0)   reads build/ca/<gen>/results.txt, prints text/data line counts
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
gen = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
rows = [l.split() for l in open(os.path.join(ROOT, 'build', 'ca', gen, 'results.txt'))]
rows = [r for r in rows if int(r[0]) <= limit]
paths = [os.path.join(ROOT, 'build', 'ca', gen, r[3]) for r in rows]
if paths:
    out = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'wip', 'dehint', 'caobj.py')] + paths, capture_output=True, text=True).stdout
    res = dict(re.findall(r'^(v\d+\.c) (text \d+ data \d+)', out, re.M))
    for r in rows:
        print(r[0], r[1], r[2], r[3], res.get(r[3], '?'))
