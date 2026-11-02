import re,sys
sys.argv=['comb.py']
exec(open('comb.py').read().split("if __name__")[0])
fix=['','n00_t4','n00_t5','n00_s4','n02_t4','n02_t5','n02_s4','s07_i0','s08_i0','s09_i0','s13_i0']
B=open('b0.c').read()
c11=[('k4',B)]
# vary c11 dead-entry conjunct count
base3='__builtin_constant_p(mode + 2400) && __builtin_constant_p(mode + 52400) && __builtin_constant_p(mode + 102400) && __builtin_constant_p(mode + 152400)) goto c11'
for k,extra in [('k3',None),('k5',' && __builtin_constant_p(mode + 202400)'),('k6',' && __builtin_constant_p(mode + 202400) && __builtin_constant_p(mode + 252400)')]:
    if extra is None: s=B.replace(base3,'__builtin_constant_p(mode + 2400) && __builtin_constant_p(mode + 52400) && __builtin_constant_p(mode + 102400)) goto c11')
    else: s=B.replace(base3,base3[:-10]+extra+') goto c11')
    c11.append((k,s))
for kn,src in c11:
  for f in fix:
    e=[parse(f)] if f else []
    open('y/%s_%s.c'%(kn,f or 'none'),'w',newline='\n').write(apply(src,e))
