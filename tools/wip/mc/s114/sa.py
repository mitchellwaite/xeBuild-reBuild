# sa.py seed n start.c : SA over dead __builtin_constant_p(mode+K) chains: conj count, shared first constant (collision), case-6 asm goto label
import re, sys, random, subprocess, os, math, shutil
S = os.path.dirname(os.path.abspath(__file__)); seed = sys.argv[1]; random.seed(int(seed)); N = int(sys.argv[2])
t0 = open(sys.argv[3]).read()
t0 = t0.replace('__asm__ goto ("" :::: c11); break;', 'break;')
CH = list(re.finditer(r'if \(__builtin_constant_p\(mode \+ (\d+)\)( && __builtin_constant_p\(mode \+ \d+\))*\) (goto \w+|mode = \d+)', t0))
base = [m.group(0).count('__builtin_constant_p') for m in CH]
A = [int(m.group(1)) for m in CH]
LB = [None, 'c11', 'c1', 'c2', 'c3', 'c7', 'c8', 'c9', 'c10', 'c12', 'cdef']
def build(cfg):
    cn, sh, c6 = cfg; out = []; last = 0
    for k, (m, n) in enumerate(zip(CH, cn)):
        out.append(t0[last:m.start()]); last = m.end()
        a = A[k]; ks = [a + 50000 * i for i in range(n)]
        if sh[k] is not None: ks[0] = A[sh[k]]
        out.append('if (' + ' && '.join('__builtin_constant_p(mode + %d)' % x for x in ks) + ') ' + m.group(3))
    t = ''.join(out) + t0[last:]
    if c6: t = t.replace('case 6:\n\t\t\t\tbreak;', 'case 6:\n\t\t\t\t__asm__ goto ("" :::: %s); break;' % c6, 1)
    return t
def f2(cfg, tag):
    p = '%s/sa%s/%s.c' % (S, seed, tag)
    open(p, 'w', newline='\n').write(build(cfg)); shutil.copy(S + '/b0.ref', p[:-2] + '.ref')
    r = subprocess.run(['sh', S + '/../s101/f2.sh', p], capture_output=True, text=True).stdout.strip()
    return int(r or 9999)
os.makedirs('%s/sa%s' % (S, seed), exist_ok=True)
ci = [i for i, m in enumerate(CH) if m.group(3) == 'goto c11'][-1]
cn0 = list(base); cn0[ci] = int(sys.argv[4]) if len(sys.argv) > 4 else 4
cur = (cn0, [None] * len(CH), sys.argv[5] if len(sys.argv) > 5 else 'c11')
c = f2(cur, 'cur'); best = c; log = open('%s/sa%s.log' % (S, seed), 'w'); log.write('start %d\n' % c)
for it in range(N):
    T = 5.0 * (1 - it / N) + 0.3
    cn, sh, c6 = list(cur[0]), list(cur[1]), cur[2]
    for _ in range(random.choice((1, 1, 2))):
        r = random.random(); i = random.randrange(len(cn))
        if r < 0.6: cn[i] = max(1, min(14, cn[i] + random.choice((-1, 1))))
        elif r < 0.9: sh[i] = None if sh[i] is not None else random.randrange(len(cn))
        else: c6 = random.choice(LB)
    nw = (cn, sh, c6); d = f2(nw, 'try')
    if d <= c or random.random() < math.exp(-(d - c) / T): cur, c = nw, d
    if d < best:
        best = d; open('%s/sa%s/best_%d.c' % (S, seed, d), 'w', newline='\n').write(build(nw))
    log.write('%d %d %d %d %s %s %s\n' % (it, d, c, best, nw[0], nw[1], nw[2])); log.flush()
