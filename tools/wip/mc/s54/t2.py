import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2
for order in (['u2'],['cdef'],['c1'],['p0'],['c12','u2'],['s5']):
    r=es2.run(rkgen.mk({},order=order),'s54a'); print(order,r['es2'],r['per2'],r['score'])
