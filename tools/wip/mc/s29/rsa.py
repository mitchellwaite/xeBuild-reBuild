"""rsa.py OUT SEED ITERS : SA over real plain compiles. State: rok JMP lists J1,J2, E toggles on option
tests, RX126/RX117. Score = true inversions (ev.score_order) of the round-4 order."""
import sys, re, json, random, math, m, ev
out, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
TAG = 'rsa%d' % seed
s0 = open('best_g7b_dup.c').read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
C4 = 'case 4:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'; C5 = 'case 5:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'
s0 = s0.replace(C4, 'case 4:\n\t\t\t\th4t: if (cinfo->hwFlags & 0x20)').replace(C5, 'case 5:\n\t\t\t\th5t: if (cinfo->hwFlags & 0x20)')
L = ['c12', 'c11', 'p0', 'i0', 'c9', 'hdd4', 'hdd5', 'c2', 'c1', 'c10', 'u2', 'cdef', 'c8', 'c7', 'c3', 's5', 's4', 'p1', 'i1', 'h4t', 'h5t']
L0 = s0.index('for (i = 0; i < argc; i++) {', s0.index('int mode_client('))
TS = [(L0 + mm.start(), mm.group(0), mm.group(2), bool(mm.group(1))) for mm in
      re.finditer(r'if \((E\()?(!strnicmp\(argv\[i\], "[^"]+", \d+\))\)?\)', s0[L0:L0 + 6000])]
R117o = '{ AT(p0) clientPatches(NULL); JUMP(i0); }'
def build(st):
    t = s0
    for i in sorted(st['E'], reverse=True):
        p, full, inner, has = TS[i]
        t = t[:p] + ('if (%s)' % inner if has else 'if (E(%s))' % inner) + t[p + len(full):]
    rep = ''
    if st['J1']: rep += 'JMP(%s); ' % ','.join(st['J1'])
    if st['J2']: rep += 'JMP(%s); ' % ','.join(st['J2'])
    t = t.replace(A, rep or ';')
    if st['R1']:
        p = t.rindex('JUMP(efail); }'); t = t[:p] + 'JMP(efail); }' + t[p + len('JUMP(efail); }'):]
    if st['R2']: t = t.replace(R117o, R117o.replace('JUMP(i0)', 'JMP(i0)'))
    return t
def score(st):
    r = m.meas(build(st), TAG)
    if 'err' in r: return 999, ''
    s, miss, o = ev.score_order(r['order'].split()[1:])
    return s + 5 * len([b for b in miss if b not in ev.CASES]), r['order']
def mut(st):
    st = json.loads(json.dumps(st)); k = random.random()
    if k < 0.3:
        x = random.choice(L); j = st['J1']; (j.remove(x) if x in j else j.insert(random.randint(0, len(j)), x))
    elif k < 0.45:
        x = random.choice(L); j = st['J2']; (j.remove(x) if x in j else j.insert(random.randint(0, len(j)), x))
    elif k < 0.85:
        i = random.randrange(len(TS)); e = st['E']; (e.remove(i) if i in e else e.append(i))
    elif k < 0.92: st['R1'] = not st['R1']
    else: st['R2'] = not st['R2']
    return st
random.seed(seed)
st = {'J1': [], 'J2': [], 'E': [], 'R1': False, 'R2': False}
if len(sys.argv) > 4: st = json.loads(sys.argv[4])
cur, o = score(st); best = cur; T = 3.0
fo = open(out, 'a')
for it in range(iters):
    nst = mut(st)
    if random.random() < 0.3: nst = mut(nst)
    x, o = score(nst)
    fo.write(json.dumps([x, nst, o]) + '\n'); fo.flush()
    if x <= cur or random.random() < math.exp((cur - x) / T): st, cur = nst, x
    if x < best: best = x; print(it, x, json.dumps(nst), o, flush=True)
    T = max(0.5, T * 0.999)
