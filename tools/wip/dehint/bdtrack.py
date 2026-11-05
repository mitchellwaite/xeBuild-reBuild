"""python tools/wip/dehint/bdtrack.py dumpdir fn regex: after each tree pass (dumps from bdpasses.py), the frequencies of fn's blocks with a line matching regex."""
import os, re, sys

d, fn, rx = sys.argv[1:4]
names = [n for n in os.listdir(d) if re.search(r'\.\d+t\.', n)]
names.sort(key=lambda n: int(re.search(r'\.(\d+)t\.', n).group(1)))
prev = None
for n in names:
    on = seen = False
    cur, hits = None, []
    for l in open(os.path.join(d, n), errors='replace'):
        if l.startswith(';; Function '):
            on = l.split()[2] == fn
            seen = False
            continue
        if on and l.startswith(fn + ' ('):
            seen = True
        if on and seen:
            m = re.match(r';;   basic block (\d+),.*freq (\d+)', l)
            if m:
                cur = (m.group(1), m.group(2))
            elif cur and re.search(rx, l):
                hits.append('%s:%s' % cur)
    if hits != prev:
        print(n.split('.', 1)[1], ' '.join(hits))
    prev = hits
