"""mode_client attempt 16: write a state = BASE_k0 with one mc9rep family variant applied,
the vrp1 block count corrected (mc15k.add, k = 205 - c7 thread target) and save both texts.

python tools/wip/dehint/mc16state.py BASE_k0.c FAMILY N OUT  (writes OUT_k0.c and OUT.c)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc9rep, mc12vrp, mc14filt, mc15k

t = mc1lib.read_src(sys.argv[1])
fam, n, out = sys.argv[2], int(sys.argv[3]), sys.argv[4]
x = dict(mc14filt.gens(t, [fam]))['%s %d' % (fam, n)] if fam != 'none' else t
k = 205 - mc14filt.c7x(mc12vrp.threads(x))
y = mc15k.add(x, k)
open(out + '_k0.c', 'w', newline='\n').write(x)
open(out + '.c', 'w', newline='\n').write(y)
print('k', k, mc1lib.fmt(mc1lib.score_text(y, [])))
