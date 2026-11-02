import sys; sys.path.insert(0,'../s86'); import r4sim
for d in sys.argv[1:]:
    pre,g,first=r4sim.load('dd/%s/mc.bbro'%d); print(d, ' '.join(map(str,first[:60])))
