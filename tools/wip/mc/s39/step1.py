"""step1.py: site table. g7b + one JMP(site -> fixed target); record key deltas, inv, fncmp."""
import json, sys, m, voc, ev
from multiprocessing import Pool
G = json.load(open('g7b.json'))
def keys(r): return {k: tuple(map(int, v.split('/'))) for k, v in (x.split(':') for x in r['raw'][3].split()[1:])}
def tgt(site):
    reg = voc.SITES[site][3]
    ok = voc.targets_for(site)
    for t in (['cdef', 'c11', 'c2'] if reg == 'mc' else ['einv', 'eout', 'efail']):
        if t in ok: return t
def job(a):
    i, site = a
    if site is None: ed = G
    else: ed = G + [(site, [tgt(site)])]
    r = m.meas(voc.make(ed, dupl=True), 's1_%d' % i, fncmp=True)
    if 'err' in r: return {'site': site, 'err': r['err'][-200:]}
    return {'site': site, 'tgt': site and tgt(site), 'inv': ev.score_order(r['order'].split()[1:])[0], 'fncmp': r['fncmp'],
            'keys': keys(r), 'order': r['order']}
if __name__ == '__main__':
    sites = [s for s in voc.SITES if voc.SITES[s] is not None and s != 'rok<']
    res = Pool(8).map(job, list(enumerate([None] + sites)))
    base = res[0]
    for x in res[1:]:
        if 'err' in x: continue
        x['dP'] = {k: (base['keys'].get(k), v) for k, v in x['keys'].items() if base['keys'].get(k) != v}
        x['same'] = x['order'] == base['order']
        print(x['site'], x['tgt'], 'inv', x['inv'], 'fn', x['fncmp'], 'same' if x['same'] else '', x['dP'])
    json.dump(res, open('sites.json', 'w'), indent=0)
