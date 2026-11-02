import sys
sys.argv=['comb.py']
exec(open('comb.py').read().split("if __name__")[0])
T=open('b0.c').read()
tg='c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail'.split()
for i in range(21):
  for t in tg:
    open('q/s%02d_%s.c'%(i,t),'w',newline='\n').write(apply(T,[parse('n00_t4'),('s',i,t)]))
for i in range(32):
  for t in tg:
    if i==0 and t=='t4': continue
    open('q/n%02d_%s.c'%(i,t),'w',newline='\n').write(apply(T,[parse('n00_t4'),('n',i,t)]))
