# gen4.py: dilute the first rok asm goto (all labels x m via fresh forwarders) + add single u2/hdd4/hdd5 edges
import os, re
s = open('b18.c').read()
m0 = re.search(r'__asm__ goto \(\"\" :::: (dsp, c1, c12[^)]*)\); goto rkn0;', s)
labels = [x.strip() for x in m0.group(1).split(',')]
os.makedirs('y', exist_ok=True); n = 0
for m in (2, 3, 4):
    for add in ((), ('u2',), ('hdd4', 'hdd5'), ('u2', 'hdd4', 'hdd5'), ('p0', 'i0')):
        lst = list(labels); fw = []
        for j in range(1, m):
            for l in labels:
                nm = 'dz%d_%s' % (j, l); lst.append(nm)
                tgt = ('o' + l) if l.startswith('rk') else l
                fw.append('%s: goto %s;' % (nm, tgt))
        for a in add:
            lst.append('dza_' + a); fw.append('dza_%s: goto %s;' % (a, a))
        rep = '__asm__ goto ("" :::: %s); goto rkn0; %s' % (', '.join(lst), ' '.join(fw))
        t = s.replace(m0.group(0), rep, 1)
        open('y/m%d_%s.c' % (m, '_'.join(add) or 'none'), 'w', newline='\n').write(t); n += 1
print(n, labels)
