import os, re, itertools
s = open('b18.c').read()
T = ['u2', 'hdd4', 'hdd5', 'p0', 'i0', 'c11']
os.makedirs('x', exist_ok=True); n = 0
for r in (2, 3):
    for c in itertools.combinations(T, r):
        t = s
        for k, l in zip((11, 12, 13), c): t = t.replace('ork%d: goto rkE;' % k, 'ork%d: goto %s;' % (k, l), 1)
        open('x/c_%s.c' % '_'.join(c), 'w', newline='\n').write(t); n += 1
for k in range(0, 11):
    m = re.search(r'ork%d: goto (\w+);' % k, s)
    for l in ('u2', 'hdd4', 'hdd5'):
        open('x/o%d_%s.c' % (k, l), 'w', newline='\n').write(s.replace(m.group(0), 'ork%d: goto %s;' % (k, l), 1)); n += 1
print(n)
