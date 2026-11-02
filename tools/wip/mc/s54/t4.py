import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2
for l in rkgen.RL:
    r=es2.run(rkgen.mk({},order=[l]),'s54a'); print(l,r['es2'],r['per2'],r['score'])
