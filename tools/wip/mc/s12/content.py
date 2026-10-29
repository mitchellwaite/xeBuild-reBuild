"""content.py DIFF: unbalanced lines of a fncmp diff (0 = same block contents, order only)"""
import sys
from collections import Counter
c = Counter()
for l in open(sys.argv[1]):
    if l[:1] in '+-' and l[:3] not in ('---', '+++'):
        c[l[1:].strip()] += 1 if l[0] == '+' else -1
u = {k: v for k, v in c.items() if v}
print(sum(abs(v) for v in u.values()), u if len(sys.argv) > 2 else '')
