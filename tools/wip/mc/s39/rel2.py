"""rel2.py TAG STEPS BEAM: greedy/beam multi-relocation of insertion events (hsim)."""
import sys, os, copy
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, '.')
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc39', 'slot_' + sys.argv[1])); f, P = hsim.measured(k)
def strip(R, b):
    R2 = copy.deepcopy(R); ks = []
    for ri in range(len(R2)):
        for g, evs in R2[ri]['g'].items():
            n = []
            for e in evs:
                if e[0] == 'ins' and e[2] == b: ks.append(e[3]); continue
                if e[0] == 'push' and e[1] == b: continue
                if e[0] == 'chg' and e[1] == b: ks.append(e[2]); continue
                n.append(e)
            R2[ri]['g'][g] = n
    return R2, ks
def moves(R):
    blocks = set(e[2] for r in R for evs in r['g'].values() for e in evs if e[0] == 'ins')
    for b in sorted(blocks):
        R2, ks = strip(R, b)
        for ri in range(len(R2)):
            for g in list(R2[ri]['g']):
                for K in set(ks):
                    for where in ('next', 'this'):
                        R3 = copy.deepcopy(R2); R3[ri]['g'][g] = R3[ri]['g'][g] + [('ins', where, b, K)]
                        yield (b, ri, g, K, where), R3
beam = [(pot.tinv(hsim.sim(R, f, P)), [], R)]
for step in range(int(sys.argv[2])):
    cand = []
    for sc, hist, Rb in beam:
        for mv, R3 in moves(Rb):
            try: o = hsim.sim(R3, f, P)
            except Exception: continue
            cand.append((pot.tinv(o), hist + [mv], R3, ' '.join(map(str, o))[:150]))
    cand.sort(key=lambda z: z[0]); seen = set(); beam = []
    for c in cand:
        if c[3] in seen: continue
        seen.add(c[3]); beam.append(c[:3])
        if len(beam) == int(sys.argv[3]): break
    print('step', step)
    for c in cand[:6]: print('  ', c[0], c[1], c[3])
    sys.stdout.flush()
