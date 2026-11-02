# gen2.py: retarget rok fan slots (orkN: goto rkE) to the prof rok JUMP targets missing from ours
import os, re, itertools
s = open('b18.c').read()
slots = [int(x) for x in re.findall(r'ork(\d+): goto rkE;', s)]
T = ['p0', 'i0', 'u2', 'hdd4', 'hdd5', 'c11']
os.makedirs('w', exist_ok=True); n = 0
for t in T:
    for k in slots:
        open('w/%s_%d.c' % (t, k), 'w', newline='\n').write(s.replace('ork%d: goto rkE;' % k, 'ork%d: goto %s;' % (k, t), 1)); n += 1
# all six at once, spread over first slots / last slots
for nm, sl in (('all6a', slots[:6]), ('all6b', slots[-6:]), ('all6c', slots[::3][:6])):
    t2 = s
    for k, t in zip(sl, T): t2 = t2.replace('ork%d: goto rkE;' % k, 'ork%d: goto %s;' % (k, t), 1)
    open('w/%s.c' % nm, 'w', newline='\n').write(t2); n += 1
print(n, slots)
