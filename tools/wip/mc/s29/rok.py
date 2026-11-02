import sys, m, ev
src = open('best_g7b_dup.c').read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
assert A in src
for tag, rep in [(a, b) for a, b in [x.split('=', 1) for x in sys.argv[1:]]]:
    t = src.replace(A, rep)
    r = m.meas(t, tag, fncmp=True)
    if 'err' in r: print(tag, 'ERR', r['err'][-300:]); continue
    print(tag, ev.score_order(r['order'].split()[1:])[0], r['inv'], r.get('fncmp'), r['order'], flush=True)
