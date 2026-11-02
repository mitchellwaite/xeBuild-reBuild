import itertools, lev, os
os.makedirs('g1', exist_ok=True)
for wb3, w4, c11, k, e, pf, ps in itertools.product(['b','2','n'], [0,3], [3,4], [2,1], [1,0], range(-1,8), range(-1,8)):
    if (pf >= 0) + (ps >= 0) == 2 and not (pf in (5,6,7,0) and ps in (5,6,7,0)): continue
    cfg = dict(wb3=wb3, wb4=w4, c11=c11, k=k, e=e, pf=pf, ps=ps)
    n = lev.name(cfg); open('g1/v_%s.c' % n, 'w', newline='\n').write(lev.apply(cfg)); print(n)
