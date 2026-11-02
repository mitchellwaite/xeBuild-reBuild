import sys, itertools, json, m, ev
src = open('best_g7b_dup.c').read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
L = ['c12', 'c11', 'p0', 'i0', 'c9', 'hdd4', 'hdd5', 'c2', 'c1', 'c10', 'u2', 'cdef', 'c8', 'c7', 'c3', 's5', 's4', 'p1', 'i1']
out = open(sys.argv[1], 'a')
K = int(sys.argv[2])
for n in range(K, K + 1):
    for T in itertools.combinations(L, n):
        rep = A + ' JMP(%s);' % ','.join(T)
        r = m.meas(src.replace(A, rep), 'rs', fncmp=False)
        if 'err' in r: continue
        s = ev.score_order(r['order'].split()[1:])[0]
        out.write(json.dumps([s, T, r['order']]) + '\n'); out.flush()
