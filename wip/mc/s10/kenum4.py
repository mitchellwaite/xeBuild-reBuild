"""nonincreasing enumeration with a 'never executed' level (-1 -> key BB_FREQ_MAX).
python kenum4.py bbro C [tailset]"""
import sys, os
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fibsim, fibwhatif, mcsim3 as mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
C = float(sys.argv[2])
SEQ = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
TAIL = [73, 81, 86, 137, 95, 138, 96, 91, 93]
LO = lambda t: max(0.0, t - 0.5)
def ok(x):
    if LO(x[112]) > C / 2 or LO(x[115]) > C / 2: return False
    a = LO(x[127]); b = LO(x[126]); c = LO(x[125])
    if b > (C - a) / 2 + 1e-9 or c > (C - a - b) / 2 + 1e-9: return False
    return True
n = [0]; best = [99]
def rec(i, hi, x):
    if i == len(SEQ):
        if not ok(x): return
        for tv in (None, -1):
            y = dict(x)
            if tv is not None: y.update({t: tv for t in TAIL})
            n[0] += 1
            o = mcsim2.sim(R, y); pre, inv, oo = mcsim2.score(o, npre)
            if inv < best[0]: best[0] = inv; print(inv, pre, y, flush=True)
            if inv == 0: print('PERFECT', y, ' '.join(map(str, oo)), flush=True); sys.exit()
        return
    b = SEQ[i]
    for v in range(hi, -2, -1):
        if b in (112, 115) and LO(v) > C / 2: continue
        x[b] = v; rec(i + 1, v, x)
    x.pop(b, None)
rec(0, 9, {})
print('n', n[0], 'best', best[0])
