"""python tools/wip/dehint/irrl13.py <irwin3 output>: run-length the windows (attempt 13)."""
import sys
for l in open(sys.argv[1]).read().split('\n'):
    t = l.split()
    if len(t) < 3 or ':' not in t[1] or t[0] == 'base':
        print(l[:80]); continue
    out, prev = [], None
    for x in t[1:]:
        p, v = x.split(':', 1)
        if v != prev:
            out.append(p + ':' + v); prev = v
    print(t[0], ' '.join(out)[:400])
