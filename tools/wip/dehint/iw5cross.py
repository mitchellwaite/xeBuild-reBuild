"""python tools/wip/dehint/iw5cross.py base1.c base2.c ...: on each base, with and without imgAddFile's len++ test, every subset of {c4, opt, pin_t}.
Prints the results sorted by lines (no --param)."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iw5

F = '	if (imgFits(off, len)) {\n		fsFiles'
L = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
jobs = []
for b in sys.argv[1:]:
    t = open(b, newline='').read().replace('\r\n', '\n')
    for useL in (0, 1):
        for k in range(4):
            for c in itertools.combinations(('c4', 'opt', 'pin_t'), k):
                s = t
                if useL and L + F not in s:
                    s = s.replace(F, L + F)
                if not useL:
                    s = s.replace(L + F, F)
                jobs.append((os.path.basename(b), useL, c, iw5.apply(s, c)))


def run(j):
    return j, iwlib.score_text(j[3], [])


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(run, jobs))
res.sort(key=lambda x: x[1].get('total', 1 << 30))
for j, r in res[:30]:
    print(j[0], 'L' if j[1] else '-', ','.join(j[2]) or '-', iwlib.fmt(r)[:120])
