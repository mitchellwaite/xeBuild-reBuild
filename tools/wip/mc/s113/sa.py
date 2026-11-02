# sa.py seed n : SA over conj counts of every dead __builtin_constant_p goto chain in b0.c (+ optional empty asm gotos)
import re, sys, random, subprocess, os, math
S = os.path.dirname(os.path.abspath(__file__)); random.seed(int(sys.argv[1])); N = int(sys.argv[2])
t0 = open(S + '/b0.c').read()
CH = list(re.finditer(r'if \(__builtin_constant_p\(mode \+ (\d+)\)( && __builtin_constant_p\(mode \+ \d+\))*\) (goto \w+|mode = \d+)', t0))
base = [m.group(0).count('__builtin_constant_p') for m in CH]
JM = [('case 6:\n\t\t\t\tbreak;', 'case 6:\n\t\t\t\t__asm__ goto ("" :::: %s); break;'),
      ('{ AT(p1) clientPatches(arg); }', '{ AT(p1) clientPatches(arg); __asm__ goto ("" :::: %s); }'),
      ('{ AT(i1) clientInfo(arg); }', '{ AT(i1) clientInfo(arg); __asm__ goto ("" :::: %s); }'),
      ('AT(c2) clientWrite(arg);\n', 'AT(c2) clientWrite(arg); __asm__ goto ("" :::: %s);\n'),
      ('JMP(p1,cdef); }', 'JMP(p1,cdef); __asm__ goto ("" :::: %s); }')]
LB = ['c11', 'c1', 'c2', 'c3', 'c7', 'c8', 'c9', 'c10', 'c12', 'cdef', 's5', 't4', 't5']
def build(cfg):
    cn, jm = cfg; t = t0; out = []; last = 0
    for m, n in zip(CH, cn):
        out.append(t[last:m.start()]); last = m.end()
        a = int(m.group(1)); tail = m.group(3)
        if n == m.group(0).count('__builtin_constant_p'): out.append(m.group(0)); continue
        out.append('if (' + ' && '.join('__builtin_constant_p(mode + %d)' % (a + 50000 * i) for i in range(n)) + ') ' + tail)
    t = ''.join(out) + t[last:]
    for i, l in enumerate(jm):
        if l: a, b = JM[i]; t = t.replace(a, b % l)
    return t
def f2(cfg, tag):
    p = '%s/sa%s/%s.c' % (S, sys.argv[1], tag)
    open(p, 'w', newline='\n').write(build(cfg))
    import shutil; shutil.copy(S + '/b0.ref', p[:-2] + '.ref')
    r = subprocess.run(['sh', S + '/../s101/f2.sh', p], capture_output=True, text=True).stdout.strip()
    return int(r or 9999)
os.makedirs('%s/sa%s' % (S, sys.argv[1]), exist_ok=True)
ci = [i for i, m in enumerate(CH) if m.group(3) == 'goto c11'][0]
cur = (list(base), [None] * len(JM)); cur[0][ci] = 4
c = f2(cur, 'cur'); best = c; log = open('%s/sa%s.log' % (S, sys.argv[1]), 'w')
for it in range(N):
    T = 6.0 * (1 - it / N) + 0.3
    cn, jm = list(cur[0]), list(cur[1])
    for _ in range(random.choice((1, 1, 2))):
        if random.random() < 0.8:
            i = random.randrange(len(cn)); cn[i] = max(1, min(14, cn[i] + random.choice((-1, 1))))
        else:
            i = random.randrange(len(JM)); jm[i] = None if jm[i] else random.choice(LB)
    nw = (cn, jm); d = f2(nw, 'try')
    if d <= c or random.random() < math.exp(-(d - c) / T): cur, c = nw, d
    if d < best:
        best = d; open('%s/sa%s/best_%d.c' % (S, sys.argv[1], d), 'w', newline='\n').write(build(nw))
    log.write('%d %d %d %d %s %s\n' % (it, d, c, best, nw[0], nw[1])); log.flush()
