import json, sys, m, voc, ev
from multiprocessing import Pool
from step1 import G, keys
def job(a):
    i, ed = a
    r = m.meas(voc.make(G + ed, dupl=True), 'pr_%d' % i, fncmp=True)
    if 'err' in r: return None
    return ed, ev.score_order(r['order'].split()[1:])[0], r['fncmp'], keys(r), r['order']
if __name__ == '__main__':
    jobs = json.loads(sys.argv[1])
    res = Pool(8).map(job, list(enumerate(jobs)))
    b = job((99, []))
    for x in res:
        if x is None: print('ERR'); continue
        print(x[0], 'inv', x[1], 'fn', x[2], {k: (b[3].get(k), v) for k, v in x[3].items() if b[3].get(k) != v}, 'SAME' if x[4] == b[4] else '')
