import sys; sys.path.insert(0,'.')
import m, loopsites as L
t=open('best_g7b_dup.c').read()
for tag,site,tg in [('base',None,None),('sig1','sig',['hdd4']),('keys1','keys',['hdd4'])]:
    x=t if not site else L.add(t,site,tg)
    r=m.meas(x,tag,True); print(tag,r.get('inv'),r.get('fncmp'),r.get('order'),r.get('err','')[:300])
