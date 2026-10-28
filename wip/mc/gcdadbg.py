"""Debug re/gcda.py's view of one function: its gcno arcs (tree/fake flags), the gcno->dump block
map, the arc and block flows (entry = 1) after overrides, and the counters written to a .gcda.
python wip/mc/gcdadbg.py <-.gcno> <m.c.042t.profile_estimate> <-.gcda> <function> [fn:src>dst=p ...]
(the first two live in the directory wip/mcfdo.py prepared, the .gcda in one of its slot dirs)"""
import struct, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 're'))
import gcda

gcno, dump, out, fname = sys.argv[1:5]
over = {}
for a in sys.argv[5:]:
    import re
    m = re.match(r'(\w+):(\d+)>(\d+)=([\d.]+)$', a)
    over.setdefault(m.group(1), {})[(int(m.group(2)), int(m.group(3)))] = float(m.group(4))
version, stamp, fns = gcda.read_gcno(gcno)
fn = [f for f in fns if f['name'] == fname][0]
est, calls = gcda.read_dump(dump)
print('gcno blocks', fn.get('nblocks', '?'), 'arcs:')
for s, d, f in fn['arcs']:
    print('  %d->%d%s' % (s, d, ' (tree)' if f & gcda.ON_TREE else '') + (' fake' if f & gcda.FAKE else ''))

fl = gcda.flows(fn, est[fname], over.get(fname, {})); print('map gcno block -> dump bb:', fn.get('map'))
print('arc flows (entry=1):')
for k, v in sorted(fl[0].items()):
    print('  %s: %.4f' % (k, v))
print('block flows:', {k: round(v, 4) for k, v in sorted(fl[1].items())})
# counters written for this function
d = open(out, 'rb').read()
w = struct.unpack('<%dI' % (len(d) // 4), d)
i = 3
while i < len(w):
    tag, n = w[i], w[i + 1]
    rec = w[i + 2:i + 2 + n]
    if tag == gcda.T_FUNCTION:
        ident = rec[0]
    elif tag == gcda.T_COUNTER_ARCS and ident == fn['ident']:
        ctr = [rec[j] | (rec[j + 1] << 32) for j in range(0, len(rec), 2)]
        arcs = [(s, dd) for s, dd, f in fn['arcs'] if not f & gcda.ON_TREE]
        print('counters:', list(zip(arcs, ctr)))
    i += 2 + n
