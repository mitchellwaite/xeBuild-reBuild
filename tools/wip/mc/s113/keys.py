# keys.py dmpdir : round-4 pop order with last key (prio,freq) and label/callee
import sys, re
d = sys.argv[1]; t = open(d + '/mc.bbro').read()
i4 = t.index('STC - round 4')
pre = t[:i4]
key = {}
for m in re.finditer(r'start of (?:next|this) round: (\d+) \(key: (-?\d+)\)|Changing key for bb (\d+) from -?\d+ to (-?\d+)', pre):
    b = int(m.group(1) or m.group(3)); k = int(m.group(2) or m.group(4)); key[b] = k
info = {}
for l in open(d + '/../' + d.split('dmp_')[-1] + '.bbinfo'):
    f = l.split()
    if len(f) > 3 and f[1] == "old" and f[2].isdigit(): info[int(f[2])] = ' '.join(x for x in f[6:] if not x.startswith('L') and not x.startswith('*'))[:20]
tr = re.findall(r'Trace \d+ \(round 4\):\s+(\d+)', t)
out = []
for b in tr:
    b = int(b); k = key.get(b)
    if k is None: s = '?'
    elif k <= -1000000: v = -k - 1000000; s = '(%d,%d)' % (v // 100, v % 100)
    else: s = '(-,%d)' % -k
    out.append('%d%s%s' % (b, s, ':' + info.get(b, '') if info.get(b) else ''))
print(' '.join(out))
