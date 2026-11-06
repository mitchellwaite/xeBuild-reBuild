"""mode_client attempt 16: apply list edits (mc8comp.edits indices) to BASE_k0, correct the
block count (mc15k) and print score and case keys.

python tools/wip/dehint/mc16le.py BASE_k0.c IDX[,IDX...] [OUT.c]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l, mc8comp, mc12vrp, mc12keys, mc14filt, mc15k

t = mc1lib.read_src(sys.argv[1])
for i in sorted((int(x) for x in sys.argv[2].split(',')), reverse=True):
    d, ed = mc8comp.edits(t)[i]
    print('edit', d)
    t = mc7j2l.apply(t, ed)
k = 205 - mc14filt.c7x(mc12vrp.threads(t))
y = mc15k.add(t, k)
print('k', k, mc1lib.fmt(mc1lib.score_text(y, [])) if y else 'no k')
if y:
    kk = mc12keys.keys(y, ['c1', 'c2', 't4', 't5', 'c9', 'c11', 'c7', 'cdef'])
    print(' '.join('%s=%s[%s]T%s' % ((l,) + kk[l][:3]) for l in kk))
    if len(sys.argv) > 3:
        open(sys.argv[3], 'w', newline='\n').write(y)
