import sys
sys.path.insert(0,'../s104'); import srch, r4sim
pre,g,first=r4sim.load(sys.argv[1])
T=srch.T
print('T   ',' '.join(map(str,T)))
for a in sys.argv[2:]:
    ov=dict((int(x.split('=')[0]),int(x.split('=')[1])) for x in a.split(',') if x)
    o=srch.sim(pre,g,ov); print(a, srch.dist(o), ' '.join(map(str,o)))
