import sys
f=sys.argv[1]; sys.argv=['x',f,'0','0']
exec(open('wr2.py').read().split('random.seed')[0])
import tmap
print('base',score(r4sim.sim(pre,g,{})))
p2=[e for e in pre if not (e[0]=='push' and e[1]==146)]
o=r4sim.sim(p2,g,{}); print('nopush146',score(o))
for k in range(-12,1):
  p3=[(e if not (e[0]=='push' and e[1]==146) else ('push',146,k)) for e in pre]
  print(k,score(r4sim.sim(p3,g,{})))
