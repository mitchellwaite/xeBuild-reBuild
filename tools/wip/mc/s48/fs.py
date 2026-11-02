"""fs.py SLOT: exhaustive key (freq) overrides on round-4 blocks; true-order inversions via ev WANT."""
import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
import hsim
WANT = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67,
        127, 117, 130, 35, 42, 53, 77, 79, 73, 81, 86, 91, 93]
P = {b: i for i, b in enumerate(WANT)}
def tinv(o):
    o = [b for b in o if b in P]
    return sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if P[o[a]] > P[o[b]])
R, k = hsim.load(sys.argv[1])
if __name__ == "__main__":
    B = [int(x) for x in sys.argv[2].split(',')]
    res = []
    for vals in itertools.product(range(0, 5), repeat=len(B)):
        f = {b: v for b, v in zip(B, vals) if v}
        o = hsim.sim(R, f, {})
        res.append((tinv(o), f))
    res.sort(key=lambda r: r[0])
    print('base', tinv(hsim.sim(R, {}, {})))
    for r in res[:15]: print(r)
