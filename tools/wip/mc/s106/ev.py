import sys
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim, m
pre,g,first=r4sim.load(sys.argv[1])
want=[eval(x) for x in sys.argv[2:]]
cur=[(pre,g)]
p,gg=pre,g
for w in want:
    for e,p2,g2 in m.edits(p,gg):
        if e==w: p,gg=p2,g2; break
    else: print('noedit',w)
o=srch.sim(p,gg); print(srch.dist(o),' '.join(map(str,o)))
print('T',' '.join(map(str,srch.T)))
