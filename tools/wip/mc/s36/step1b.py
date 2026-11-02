import json, m, voc, ev, loopsites
from multiprocessing import Pool
from step1 import G, keys
def job(a):
    i, site, tg = a
    t = voc.make(G, dupl=True)
    if site: t = loopsites.add(t, site, tg)
    r = m.meas(t, 's1b_%d' % i, fncmp=True)
    if 'err' in r: return {'site': site, 'err': r['err'][-300:]}
    return {'site': site, 'tgt': tg, 'inv': ev.score_order(r['order'].split()[1:])[0], 'fncmp': r['fncmp'], 'keys': keys(r), 'order': r['order'], 'r3': r['fq'] and r['raw'][0]}
if __name__ == '__main__':
    J = [(0, None, None)] + [(i + 1, s, ['cdef']) for i, s in enumerate(loopsites.LS)]
    res = Pool(8).map(job, J); b = res[0]
    for x in res[1:]:
        if 'err' in x: print(x['site'], 'ERR', x['err'][-150:]); continue
        x['dP'] = {k: (b['keys'].get(k), v) for k, v in x['keys'].items() if b['keys'].get(k) != v}
        print(x['site'], 'inv', x['inv'], 'fn', x['fncmp'], 'SAME' if x['order'] == b['order'] else '', x['dP'])
    json.dump(res, open('sites_loop.json', 'w'), indent=0)
