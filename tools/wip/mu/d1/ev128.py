"""ev128.py DUMP B..: every heap event of the given blocks, in round order, with the visiting block."""
import sys

import dsim

M = dsim.load(sys.argv[1])
bs = set(map(int, sys.argv[2:]))
for e in M['pre']:
    if e[0] == 'ins' and e[2] in bs or e[0] in ('push', 'chg') and e[1] in bs:
        print('pre', e)
for rn, g in (('r3', M['g3']), ('r4', M['g4'])):
    for k, l in g.items():
        for e in l:
            if e[0] == 'ins' and e[2] in bs or e[0] in ('push', 'chg') and e[1] in bs:
                print(rn, 'at', k, e)
