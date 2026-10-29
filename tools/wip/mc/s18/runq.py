"""runq.py SLOT target.json [iters]   closed-loop realizer for a fake7 design on a genq variant.
env MCD = prepared build dir (genq variant, e.g. mcq1).  target.json = {'f': {sp: f}, 'P': {sp|xS_T: P}}
State (current overrides) is kept in <MCD>/slot<SLOT>/ov.json; every iteration compiles, analyzes the
real bbro dump (analyze.py) and rescales each controlling edge by target/measured."""
import json, os, subprocess, sys, re
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip\mc\s18'); sys.path.insert(0, ROOT + r'\tools\wip\mc\s12'); sys.path.insert(0, ROOT + r'\tools\wip')
import analyze, run12
MCD = os.environ.get('MCD', 'mcq1')
os.environ['MCD'] = MCD
# sp block -> tree target in the q/vY numbering
TC = {107: 114, 108: 115, 109: 116, 110: 117, 113: 120, 116: 123, 119: 126, 120: 127, 121: 128, 128: 129, 129: 130, 132: 133}
X2T = {112: 119, 115: 122, 103: 110, 117: 124, 130: 131, 107: 114, 108: 115, 109: 116, 116: 123, 119: 126, 120: 127,
       121: 128, 128: 129, 129: 130, 132: 133}
ARMT = {131: 132, 118: 125, 114: 121}    # arm blocks (zero-flow X1/X2 targets)
LOOPU = {29: 'mode_client:27>29', 33: 'mode_client:19>20', 35: 'mode_client:34>35', 53: 'mode_client:40>41',
         42: 'mode_client:42>43', 77: 'mode_client:61>62', 79: 'mode_client:77>78'}
XPRI = {}
BASE = json.load(open(ROOT + r'\tools\wip\mc\s12\startY.json'))


def defaults(tgt):
    ov = {}
    for k, v in BASE.items():
        if k.startswith('fx') or k.startswith('cw'): continue
        ov[run12.key(k)] = v
    for c in TC: ov['mode_client:113>%d' % TC[c]] = 8.0
    ov['mode_client:113>134'] = 0.0
    for t in X2T: ov['mode_client:109>%d' % X2T[t]] = 0.0
    for t in os.environ.get('X1T', '112,115,121').split(','):       # X1 (vY asm goto) carries no flow
        if t: ov['mode_client:112>%d' % {**X2T, **ARMT}[int(t)]] = 0.0
    ov['mode_client:45>49'] = 15.7; ov['mode_client:46>47'] = 17.0
    if os.environ.get('RX117') == '1': ov['mode_client:124>131'] = 0.0
    if os.environ.get('RX126', '1') == '1': ov['clientEraseBlock:7>6'] = 0.0
    ov['mode_client:107>110'] = 1.0
    ov['mode_client:108>109'] = float(os.environ.get('RPCT', '34'))
    return ov


def compile_(slot, ov):
    raw = ['%s=%.4f' % (k, v) for k, v in ov.items()]
    env = dict(os.environ, EXTRA='--param builtin-expect-probability=50', MCFDO_DIR=ROOT + '\\build\\' + MCD)
    FAKE = ['clientEraseBlock:%s>1=100' % i for i in '5 6 7 8'.split()]
    raw += FAKE + ['--consistent', '--entry=clientEraseBlock:mode_client:128']
    r = subprocess.run([sys.executable, ROOT + r'\tools\wip\mc\s9\fdorun9.py', slot, '--over'] + raw, cwd=ROOT, env=env,
                       capture_output=True, text=True)
    f = 999
    for l in r.stdout.splitlines():
        if l.startswith('fncmp'): f = int(l.split()[1])
    return f, r.stdout + r.stderr


def content(sd):
    r = subprocess.run([sys.executable, ROOT + r'\tools\wip\mc\s12\content.py', os.path.join(sd, 'fdo.diff')], capture_output=True, text=True)
    return int(r.stdout.split()[0]) if r.stdout.strip() else -1


def adj(ov, k, t, m, lo=0.0, hi=100.0):
    if k not in ov: return
    if t <= 0.05:
        if m is not None and m > 0: ov[k] = ov[k] * 0.3
    elif m is None or m <= 0.05:
        ov[k] = max(ov[k] * 2, 0.05)
    elif abs(m - t) >= 0.5:
        ov[k] = ov[k] * (t / m) ** 0.8
    ov[k] = max(lo, min(hi, ov[k]))


def step(ov, tgt, keys, named, corr):
    f, P = tgt['f'], tgt['P']
    fq = named['fq']
    def mf(b):
        if b in keys and keys[b][1] is not None and keys[b][1] >= 0: return keys[b][1]
        return fq.get(b) if fq.get(b) is not None else 0
    def mp(b):
        return keys[b][0] if b in keys and keys[b][0] is not None else 0
    D, R = float(named.get('disp') or 80), float(named.get('rok') or 30)
    # cases: dispatch part Dc and X2 part ec with P = max(Dc, ec), f = Dc + ec (+Dc for 132's range check)
    split = {}
    for c in TC:
        if c not in P: continue
        if c not in X2T:
            split[c] = (P[c] - (0.3 if f[c] >= 10 else 0.0), 0.0)
        elif c == 132:
            # prefer X2 carrying the priority (dispatch light)
            split[c] = ((f[c] - P[c]) / 2.0, float(P[c])) if f[c] - P[c] <= 2 * P[c] else (P[c], f[c] - 2 * P[c])
        else:
            lo = f[c] - P[c] - (0.35 if f[c] >= 10 else 0.0)
            split[c] = (float(P[c]), float(lo)) if not XPRI.get(c) else (float(lo), float(P[c]))
    tot = 0.0
    for c, (Dc, ec) in split.items():
        mP, mF = mp(c), mf(c)
        if c not in keys and (fq.get(c) or 0) >= 10:      # went to round 3: too hot
            corr['D%d' % c] = corr.get('D%d' % c, 1.0) * 0.93
            corr['E%d' % c] = corr.get('E%d' % c, 1.0) * 0.93
        if c in keys and Dc > 0:
            # measured dispatch part: the larger of the two parts is P (if dispatch is larger)
            mD = mP if Dc >= ec else (mF - mP if c != 132 else (mF - mP) / 2.0)
            if mD > 0 and abs(mD - Dc) >= 1:
                corr["D%d" % c] = min(1.15, max(0.85, corr.get('D%d' % c, 1.0) * (Dc / mD) ** 0.7))
        sh = 100.0 * Dc / D * corr.get('D%d' % c, 1.0) * (2.0 if c == 132 else 1.0)
        ov['mode_client:113>%d' % TC[c]] = max(0.0, sh); tot += max(0.0, sh)
        k = 'mode_client:109>%d' % X2T[c] if c in X2T and ('mode_client:109>%d' % X2T[c]) in ov else None
        if k:
            if ec <= 0: ov[k] = 0.0
            else:
                if c in keys:
                    me = mP if ec > Dc else (mF - mP)
                    if me > 0 and abs(me - ec) >= 1:
                        corr['E%d' % c] = min(2.0, max(0.5, corr.get('E%d' % c, 1.0) * (ec / me) ** 0.7))
                ov[k] = 100.0 * ec / R * corr.get('E%d' % c, 1.0)
    ov['mode_client:113>134'] = max(0.0, 100.0 - tot)
    for t in (112, 115, 103, 117, 130):
        k = 'mode_client:109>%d' % X2T[t]
        if k not in ov: continue
        want, got = P.get(t, 0), mp(t)
        ck = 'x2_%d' % t
        if want <= 0:
            ov[k] = 0.0; continue
        if t in keys and got > 0 and got != want:
            corr[ck] = min(2.0, max(0.5, corr.get(ck, 1.0) * (want / got) ** 0.7))
        elif t in keys and got <= 0:
            corr[ck] = min(2.0, corr.get(ck, 1.0) * 1.3)
        ov[k] = 100.0 * want / R * corr.get(ck, 1.0)
    x2k = [k for k in ov if k.startswith('mode_client:109>')]
    tot2 = sum(ov[k] for k in x2k)
    if tot2 > 92.0:
        print('  X2 total %.1f%% capped' % tot2)
        for k in x2k: ov[k] *= 92.0 / tot2
    for t, k in ((112, 'mode_client:117>119'), (115, 'mode_client:120>122')):
        if t in f: adj(ov, k, max(0.01, f[t] - P.get(t, 0)), max(0.01, mf(t) - mp(t)), 0.01, 50)
    if 103 in f: adj(ov, 'mode_client:107>110', max(.01, f[103] - P.get(103, 0)), max(.01, mf(103) - mp(103)), 0.01, 100)
    adj(ov, run12.key('d1'), f[117], mf(117), 0.05, 50)
    if 'mode_client:124>131' in ov:
        if P.get('x117_130'): adj(ov, 'mode_client:124>131', P['x117_130'], mp(130), 0, 100)
        else: ov['mode_client:124>131'] = 0.0
    adj(ov, run12.key('d2'), f[130] - P.get('x117_130', 0), mf(130) - mp(130), 0.05, 50)
    adj(ov, run12.key('e2'), f[127], mf(127), 0.05, 60)
    adj(ov, run12.key('e3'), f[126], mf(126), 0.05, 50)
    if 'clientEraseBlock:7>6' in ov: ov['clientEraseBlock:7>6'] = 0.0   # forced by the zero-count split anyway
    adj(ov, run12.key('e4'), f[125] - P.get('x126_125', 0), mf(125) - mp(125), 0.05, 50)
    adj(ov, run12.key('ip'), f[49], mf(49), 0.05, 60)
    F94 = f.get(94, 9)
    if named.get('k48'): adj(ov, 'mode_client:45>49', f[49] + F94, named['k48'], 1, 60)
    if named.get('b46') and named.get('k48'):
        t46 = max(11, min(named['k48'] - 2, 13))
        adj(ov, 'mode_client:46>47', t46, named['b46'], 1, 60)
    adj(ov, run12.key('r'), f[55], mf(55), 0.05, 49)
    adj(ov, run12.key('w'), f[61], mf(61), 0.05, 47)
    adj(ov, run12.key('e'), f[67], mf(67), 0.05, 49)
    for b, k in LOOPU.items():
        if b in f: adj(ov, k, f[b], mf(b), 0.0, 5)
    if 29 in f: adj(ov, 'mode_client:14>17', f[29], mf(29), 0.0, 5)



def main():
    slot, tgt = sys.argv[1], json.load(open(sys.argv[2]))
    tgt = {'f': {int(k): v for k, v in tgt['f'].items()},
           'P': {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in tgt['P'].items()}}
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    if 'd49' in tgt['P']: tgt['P'][49] = tgt['f'][49] + tgt['P']['d49']
    # move priorities onto X2 until the dispatch budget fits
    f_, P_ = tgt['f'], tgt['P']
    DMAX = float(os.environ.get('DMAX', '79'))
    def dsum():
        t = 0
        for c in TC:
            if c == 132: t += (f_[c] - P_[c]) / 2.0 if f_[c] - P_[c] <= 2 * P_[c] else P_[c]
            else: t += (f_[c] - P_[c]) if XPRI.get(c) else P_[c]
        return t
    while dsum() > DMAX:
        cands = [c for c in TC if c in X2T and c not in (110, 113, 132) and not XPRI.get(c)]
        if not cands: break
        c = max(cands, key=lambda c: 2 * P_[c] - f_[c])
        XPRI[c] = True
    print('XPRI', sorted(XPRI), 'dispatch', dsum(), flush=True)
    sd = ROOT + '\\build\\' + MCD + '\\slot' + slot
    os.makedirs(sd, exist_ok=True)
    st = os.path.join(sd, 'ov.json')
    ov = json.load(open(st)) if os.path.exists(st) else defaults(tgt)
    cs = os.path.join(sd, 'corr.json')
    corr = json.load(open(cs)) if os.path.exists(cs) else {}
    for it in range(n):
        fn, out = compile_(slot, ov)
        if fn >= 9999:
            print(out[-3000:]); break
        order, inv, keys, named = analyze.analyze(sd)
        tp = dict(tgt['P']); tp[125] = tp.get('x126_125', 0); tp[130] = max(tp.get(130, 0), tp.get('x117_130', 0))
        bad = [(b, keys.get(b), (tp.get(b, 0), tgt['f'].get(b))) for b in tgt['f']
               if b in analyze.mcsim2.pos and keys.get(b) != (tp.get(b, 0), tgt['f'][b])]
        print('it', it, 'fncmp', fn, 'content', content(sd), 'inv', inv, 'miss', len(bad), 'R', named.get('rok'), 'D', named.get('disp'), 'r3', named.get('r3'), flush=True)
        print('  order', ' '.join(map(str, order)))
        print('  bad', ' '.join('%s:%s->%s' % x for x in bad))
        json.dump(ov, open(st, 'w'), indent=0)
        if fn == 0:
            print('MATCH'); break
        if len(bad) <= int(os.environ.get('STOPMISS', '-1')):
            print('stop at miss', len(bad)); break
        step(ov, tgt, keys, named, corr)
    json.dump(ov, open(st, 'w'), indent=0); json.dump(corr, open(cs, 'w'))


if __name__ == '__main__':
    main()
