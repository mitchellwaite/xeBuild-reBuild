"""wi10.py SLOT B: relocate block B's round-4 ins to every (group,pos); also with 77/79 moved into 61 (79@2,77@3)."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s48')
from fs import tinv, hsim, R
B = int(sys.argv[2]) if len(sys.argv) > 2 else 0
def strip(g, b):
    e0 = None
    for G in g:
        for e in g[G]:
            if e[0] == 'ins' and e[2] == b: e0 = e
        g[G] = [e for e in g[G] if not (e[0] == 'ins' and e[2] == b)]
    return e0
if __name__ == "__main__":
  for mv in (0, 1):
      R1 = copy.deepcopy(R); g = R1[3]['g']
      if mv:
          e7 = strip(g, 77); e9 = strip(g, 79); g[61] = g[61][:2] + [e9, e7] + g[61][2:]
      eb = strip(g, B); res = []
      for G in g:
          for i in range(len(g[G]) + 1):
              R2 = copy.deepcopy(R1); l = R2[3]['g'][G]; R2[3]['g'][G] = l[:i] + [eb] + l[i:]
              o = hsim.sim(R2, {}, {}); res.append((tinv(o), G, i, [x for x in o if x in (103, 55, 126, 125, 61, 35, 42, 53, 77, 79)]))
      res.sort(key=lambda r: r[0]); print('mv', mv, tinv(hsim.sim(R1, {}, {})))
      for r in res[:6]: print(r)
