"""fl9g.py <label> [label..]: diff of fl9f/fl8lib states against the reference, and write the source to build/filelist_ini/a9/<n>.c
(n = position in the argument list, prefixed s), for fl9b.py and fl9c.py."""
import os, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl8lib as G, fl9f

for i, lb in enumerate(sys.argv[1:]):
    print('#####', lb)
    s = G.state(lb)
    open(os.path.join(L.BD, 'a9', 's%d.c' % i), 'w', newline='\n').write(s)
    G.show(lb, 'a9show')
