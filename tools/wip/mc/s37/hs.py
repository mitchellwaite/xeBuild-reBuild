"""hs.py SLOTTAG: hsim validation of graded case levels on a real history."""
import sys, os
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); import hsim
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116]
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc37', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
o = hsim.sim(R, f0, P0); print('measured inv', hsim.inv(o), ' '.join(map(str, o)))
def tryd(name, f, P):
    o = hsim.sim(R, f, P); print(name, 'inv', hsim.inv(o), ' '.join(map(str, o[:16])))
# A: all P4, f graded 14..4
f, P = dict(f0), dict(P0)
for i, b in enumerate(CASES): f[b] = 14 - i; P[b] = 4
tryd('A fgrade P4', f, P)
# B: P graded (distinct levels) f unchanged
f, P = dict(f0), dict(P0)
for i, b in enumerate(CASES): P[b] = 15 - i
tryd('B Pgrade', f, P)
# C: f graded only within 2 P levels (P5: 129..113, P4 rest)
f, P = dict(f0), dict(P0)
for i, b in enumerate(CASES): P[b] = 5 if i < 5 else 4; f[b] = 9 - (i % 5) if i < 5 else 10 - (i - 5)
tryd('C P5/P4 + f', f, P)
# D: f graded by +1 steps from base (realizable: base 4, up to +6)
f, P = dict(f0), dict(P0)
for i, b in enumerate(CASES): f[b] = max(f0.get(b, 4), 4) + (10 - i)
tryd('D f+steps', f, P)
