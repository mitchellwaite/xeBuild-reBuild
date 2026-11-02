# ev4.py SRC.c DIR : dump variant, map blocks to profiled, print round-4 trace heads (mapped to prof-style ids) + final-layout diff vs prof
import sys, subprocess, re, difflib
src, d = sys.argv[1], sys.argv[2]
subprocess.run(['sh', 'dump.sh', src, d], check=True)
out = subprocess.run([sys.executable, 'map.py', src, d], capture_output=True, text=True).stdout
mp = {}
for l in open('map.txt'): a, b = l.split()[:2]; mp[int(a)] = int(b)
from fin import final
o = final(d + '/mc.bbro'); p = final('pf/mc.bbro')
om = [mp.get(b, 'x%s' % b) if isinstance(b, int) else 'd' for b in o]
pm = [b if isinstance(b, int) else 'd' for b in p]
sm = difflib.SequenceMatcher(None, om, pm, autojunk=False)
print('layout-dist(prof numbering)', len(pm) - sum(x.size for x in sm.get_matching_blocks()), 'extra', sum(1 for b in om if isinstance(b, str) and b[0] == 'x'))
for t, i1, i2, j1, j2 in sm.get_opcodes():
    if t != 'equal': print(' ', t, om[i1:i2], '->', pm[j1:j2])
