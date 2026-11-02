# gen.py BASE OUT 'ln|old|new' ... : line-local substitutions (1-based line); 'Z' adds z1/z2 unreachable labels
import sys
L = open(sys.argv[1]).read().split('\n')
for s in sys.argv[3:]:
    ln, old, new = s.split('|'); ln = int(ln) - 1
    assert old in L[ln], s
    L[ln] = L[ln].replace(old, new, 1)
open(sys.argv[2], 'w', newline='\n').write('\n'.join(L))
