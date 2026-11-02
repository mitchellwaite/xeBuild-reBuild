import subprocess, sys, re, random, time, os
# gr3.py BASE.c OUT SECS [SEED] : hill climb, score = (sig2 token diff, fncmp)
# levers: bcp chain del/add/rm (not mode+260), fail-feed bcp gotos (new), rok/fkbo fan target swaps (new).
# No cold/hot label lever: `AT(l) { l_c: cold; } stmt` breaks unbraced if/else bodies (s77 finding).
src0 = open(sys.argv[1]).read(); out = sys.argv[2]
T = time.time() + float(sys.argv[3])
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else None)
os.makedirs('v', exist_ok=True)
BCP = re.compile(r'if \(((?:\(char \*\))?__builtin_constant_p\((\w+) \+ (\d+)\)(?: == (?:\(char \*\))?\d+)?(?: && (?:\(char \*\))?__builtin_constant_p\(\w+ \+ \d+\)(?: == (?:\(char \*\))?\d+)?)*)\) (goto \w+|mode = \d+);')
FEED = ['c1', 'c2', 'c3', 't4', 's4', 't5', 's5', 'c7', 'p0', 'p1', 'c8', 'c9', 'c10', 'c11', 'c12', 'i0', 'i1',
        'cdef', 'hdd4', 'hdd5', 'u2', 'dtg', 'ndl', 'efail', 'eout']
FAN = ['c1', 'c2', 'c3', 'c7', 'c8', 'c9', 'c10', 'c12', 's5', 'hdd4', 'hdd5', 'u2', 'cdef', 'i1', 'p1', 'dsp']


def cands(src):
    C = []
    for m in BCP.finditer(src):
        s = m.group(0); chain = m.group(1); var = m.group(2); act = m.group(4)
        if 'mode + 260' in s:
            continue
        parts = chain.split(' && ')
        C.append(('del', s, ''))
        n = int(re.findall(r'\+ (\d+)\)', parts[-1])[0])
        C.append(('add', s, 'if (%s && __builtin_constant_p(%s + %d)) %s;' % (chain, var, n + 50000, act)))
        if len(parts) > 1:
            C.append(('rm', s, 'if (%s) %s;' % (' && '.join(parts[:-1]), act)))
    labs = set(re.findall(r'\b(\w+):', src))
    for l in FEED:
        if l in labs:
            for k in range(2, 7):
                b = random.randint(3000, 9000)
                c = ' && '.join('__builtin_constant_p(mode + %d)' % (b + 50000 * i) for i in range(k))
                C.append(('feed', 'fail: __attribute__((cold)); ', 'fail: __attribute__((cold)); if (%s) goto %s; ' % (c, l)))
    # fan edits: rok direct list (first asm goto after rkv0) and fkbo list
    m = re.search(r'"m"\(rkv0\)\); __asm__ goto \(""(?: :){4} ([^)]*)\)', src)
    if m:
        lst = m.group(1).split(', ')
        for t in FAN:
            if t in lst:
                C.append(('rokdel', m.group(0), m.group(0).replace(m.group(1), ', '.join(x for x in lst if x != t))))
            elif t in labs:
                C.append(('rokadd', m.group(0), m.group(0).replace(m.group(1), ', '.join([t] + lst))))
    m = re.search(r'"X"\(&fkv\)\); __asm__ goto \(""(?: :){4} ([^)]*)\)', src)
    if m:
        lst = m.group(1).split(', ')
        fa = [x for x in lst if x.startswith('fa')]
        for t in FAN:
            if t in lst:
                C.append(('fkdel', m.group(0), m.group(0).replace(m.group(1), ', '.join(x for x in lst if x != t))))
            elif t in labs and len(lst) < 30:
                C.append(('fkadd', m.group(0), m.group(0).replace(m.group(1), ', '.join([t] + lst))))
            elif t in labs and fa:
                C.append(('fkswap', m.group(0), m.group(0).replace(m.group(1), ', '.join([t] + [x for x in lst if x != fa[-1]]))))
    return C


def score(s):
    p = 'v/%s_t.c' % out
    open(p, 'w', newline='\n').write(s)
    r = subprocess.run(['sh', 'f.sh', p], capture_output=True, text=True)
    try:
        f = int(r.stdout.strip())
    except ValueError:
        return (9999, 9999)
    if f >= 9999:
        return (9999, 9999)
    subprocess.run(['sh', 'ours.sh', p, 'v/%s_o.txt' % out], capture_output=True)
    r = subprocess.run(['python', 'sig2.py', 'origs.txt', 'v/%s_o.txt' % out], capture_output=True, text=True)
    d = sum(1 for l in r.stdout.split('\n') if l[:1] in '+-' and l)
    return (d, f)


cur = src0; cs = score(cur); print('base', cs, flush=True)
log = open('%s.log' % out, 'a')
rnd = 0
while time.time() < T:
    C = cands(cur); random.shuffle(C); imp = False
    for kind, o, n in C:
        if time.time() > T:
            break
        if cur.count(o) != 1:
            continue
        s = cur.replace(o, n)
        sc = score(s); log.write('%d %s %s %s\n' % (rnd, kind, sc, n[:100])); log.flush()
        if sc < cs or (sc == cs and random.random() < 0.3):
            imp = imp or sc < cs; cur, cs = s, sc; print('accept', kind, sc, n[:100], flush=True)
            open('%s_best.c' % out, 'w', newline='\n').write(cur)
            break
    rnd += 1
print('final', cs)
