import sys;sys.path.insert(0,'../s86');import r4sim
pre,g,f=r4sim.load('dd/vEa/mc.bbro')
o=r4sim.sim(pre,g,{144:-1000210,132:-1000313,108:-2})
print(' '.join(map(str,o)))
for e in pre:
  if (e[0]=='push' and e[1] in(139,96,128,105,81,79,129)) or (e[0]=='ins' and e[2] in (139,96,128,105,81,79,129)): print(e)
