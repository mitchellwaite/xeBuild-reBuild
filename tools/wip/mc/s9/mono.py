"""mcsim2 replay over every nonincreasing key assignment along WANT's cold tail.
python mono.py <mode_client bbro> [maxval]"""
import itertools, os, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 3
SEQ = [55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
best = []
def gen(n, hi):
    if n == 0: yield (); return
    for v in range(hi, -1, -1):
        for r in gen(n - 1, v): yield (v,) + r
for u2 in (3, 4):
  for hdd in (4, 5):
    for vals in gen(len(SEQ), mx):
        f = dict(zip(SEQ, vals)); f[103] = u2; f[112] = f[115] = hdd
        try: o = mcsim2.sim(R, f)
        except Exception: continue
        pre, inv, oo = mcsim2.score(o, npre)
        best.append((inv, -pre, u2, hdd, vals, oo))
        if inv == 0: print('PERFECT', u2, hdd, vals, flush=True)
best.sort()
for b in best[:8]:
    print('inv=%d pre=%d u2=%d hdd=%d %s' % (b[0], -b[1], b[2], b[3], dict(zip(SEQ, b[4])))); print('  ', ' '.join(map(str, b[5])))
