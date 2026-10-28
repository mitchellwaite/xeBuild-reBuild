import os,sys
os.environ['T48']='0'; os.environ['TX2']=''; os.environ['X1']='0'
sys.argv=['x','0','1']
import fake7
f={112:8,115:8,127:2,126:3,125:2,49:8,55:3,61:1,67:0,103:4,117:1,130:1,29:2,33:1,35:1,42:0,53:0,77:0,79:0,94:18}
P={}
for c in fake7.CASES: f[c]=6;P[c]=6
f[121]=9;P[132]=3
print(fake7.sim(f,P))
