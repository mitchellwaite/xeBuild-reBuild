import sys, m, ev, json
sys.path.insert(0, r'..\s18'); import hsim
def keys(tag):
    R, k = hsim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc29\slot_' + tag)
    f, P = hsim.measured(k)
    return {b: (f.get(b), P.get(b)) for b in [49, 94, 132, 129, 107, 115, 112, 103]}, R[2]['g'].get(1048)
src0 = open(sys.argv[1]).read()
for a in sys.argv[2:]:
    tag, ed = a.split('=', 1); src = src0
    for e in ed.split(';;'):
        o, n = e.split('=>'); assert o in src, o; src = src.replace(o, n, 1)
    r = m.meas(src, tag, fncmp=True)
    if 'err' in r: print(tag, 'ERR', r['err'][-500:]); continue
    print(tag, ev.score_order(r['order'].split()[1:])[0], r['fncmp'], r['raw'][0][:60], r['order'], keys(tag), flush=True)
