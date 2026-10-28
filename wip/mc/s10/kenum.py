"""exhaustive nonincreasing assignments along SEQ under ksearch2 constraints (C=10). python kenum.py bbro"""
import sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
SEQ = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
C = int(sys.argv[2]) if len(sys.argv) > 2 else 10
def ok(x):
    h = (C + 1) // 2
    if x[112] > h or x[115] > h: return False
    r1 = C - x[127]
    if x[126] > (r1 + 1) // 2: return False
    if x[125] > (r1 - x[126] + 1) // 2: return False
    return True
res = []
def rec(i, hi, x):
    if i == len(SEQ):
        if not ok(x): return
        o = mcsim2.sim(R, x); pre, inv, oo = mcsim2.score(o, npre)
        if inv == 0: res.append(dict(x)); print('PERFECT', x, flush=True)
        return
    b = SEQ[i]
    lo = 0
    for v in range(hi, lo - 1, -1):
        if b in (112, 115) and v > (C + 1) // 2: continue
        x[b] = v; rec(i + 1, v, x)
    x.pop(b, None)
# tail 35..79 fixed to 0 to bound the search
SEQ_FULL = SEQ; SEQ = SEQ[:14]
def rec0(i, hi, x):
    if i == len(SEQ):
        y = dict(x); y.update({35: 0, 42: 0, 53: 0, 77: 0, 79: 0})
        if not ok(y): return
        o = mcsim2.sim(R, y); pre, inv, oo = mcsim2.score(o, npre)
        if inv == 0: print('PERFECT', y, flush=True); res.append(y)
        return
    b = SEQ[i]
    for v in range(hi, -1, -1):
        if b in (112, 115) and v > (C + 1) // 2: continue
        if i >= 1 and len(res) > 20: return
        x[b] = v; rec0(i + 1, v, x)
    x.pop(b, None)
rec0(0, 10, {})
print(len(res))
if '--full' in sys.argv:
    SEQ = SEQ_FULL
    rec(0, 10, {})
    print('full', len(res))
