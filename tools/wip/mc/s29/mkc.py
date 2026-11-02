import sys
s = open('best_g7b_dup.c').read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
X2 = 'JMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
K = 'if (!strnicmp(argv[i], "-keys", 5))'; WB = 'if (E(!strnicmp(argv[i], "-wb", 3)))'
R117o = '{ AT(p0) clientPatches(NULL); JUMP(i0); }'
assert A in s and K in s and WB in s and R117o in s
def mk(name, x2=False, rx=False, t48=False):
    t = s
    if x2: t = t.replace(A, X2)
    if rx:
        p = t.rindex('JUMP(efail); }'); t = t[:p] + 'JMP(efail); }' + t[p + len('JUMP(efail); }'):]
        t = t.replace(R117o, R117o.replace('JUMP(i0)', 'JMP(i0)'))
    if t48: t = t.replace(K, 'if (E(!strnicmp(argv[i], "-keys", 5)))').replace(WB, 'if (!strnicmp(argv[i], "-wb", 3))')
    open(name, 'w', newline='\n').write(t)
mk('c_rx.c', rx=True); mk('c_x2rx.c', x2=True, rx=True); mk('c_all.c', True, True, True); mk('c_x2t.c', True, False, True); mk('c_trx.c', False, True, True)
