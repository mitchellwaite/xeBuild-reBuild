import sys
from wi import *
for d in sys.argv[1:]:
    pre,g,first=r4sim.load(d); print(d, srch.dist(first), ' '.join(map(str,first)))
