# key -3 zero-byte dummy dv: asm goto edge from the rok block (trace 105 in round 3), frequency from a dead constant_p feed + dead return
s=open('b1.c',newline='').read()
a='cinfo = netGetInfo(); if (__builtin_constant_p(mode + 620)) goto ndl;'; assert s.count(a)==1
l='__asm__ goto ("" :::: dsp, c1, c12, s5, c7, c9, c3, c8, c2, c10, cdef, rk0,'; assert s.count(l)==1
r='if (0) { dz: asm volatile("" : : : "cc"); __builtin_unreachable(); }'; assert s.count(r)==1
def cps(b,k): return ' && '.join('__builtin_constant_p(i + %d)'%(b+j) for j in range(k))
for k in (1,2,3,4):
  for lab,ln in (('first',l.replace('dsp, c1,','dv, dsp, c1,')),('mid',l.replace('rk0,','dv, rk0,'))):
    for ret,rn in ((1,'r'),(0,'n')):
      dv='if (0) { dv: asm volatile("" : : : "memory"); '+('if (__builtin_constant_p(i + 16100)) goto dvb; ' if ret else '')+'__builtin_unreachable(); } '
      x=s.replace(r,dv+r).replace(l,ln).replace(a,a+' if (%s) goto dv; '%cps(16000,k)+('dvb:; ' if ret else ''))
      open('w%d%s%s.c'%(k,lab[0],rn),'w',newline='\n').write(x)
