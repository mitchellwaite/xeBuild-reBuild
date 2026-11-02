# sw.py BASE OUT n perm : permute disjuncts of the n-th (0-based) 3-way usage condition in the arg loop
import sys, re
s = open(sys.argv[1]).read().split('\n'); n = int(sys.argv[3]); p = [int(c) for c in sys.argv[4]]
f = [i for i, x in enumerate(s) if 'for (i = 0; i < argc; i++) {' in x][0]
c = 0
for L in range(f, f + 130):
    m = re.match(r'^(\s*if \()([^|()]*|!argv\[i \+ 1\]) \|\| ([^|]*) \|\| ([^|]*)(\))$', s[L])
    if m:
        if c == n:
            d = [m.group(2), m.group(3), m.group(4)]; s[L] = m.group(1) + ' || '.join(d[j] for j in p) + m.group(5); break
        c += 1
else: raise SystemExit('none')
open(sys.argv[2], 'w', newline='\n').write('\n'.join(s))
