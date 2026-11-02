T=open('b0.c').read()
anch={'ne':'promptEnter = 0;','rb':'reboot = 2;','rd':'mode = 8;','eb':'mode = 10;','w2':'mode = 2;','m4':'mode = 4;','m5':'mode = 5;','m12':'mode = 12;','ky':'mode = 3;'}
k=500
def c1(k): return '(char *)__builtin_constant_p(i + %d) == (char *)1 && (char *)__builtin_constant_p(i + %d) == (char *)1'%(k,k+1)
def c2(k): return c1(k)+' && (char *)__builtin_constant_p(i + %d) == (char *)1 && __builtin_constant_p(i + %d)'%(k+2,k+77000)
def c3(k): return ' && '.join('__builtin_constant_p(i + %d)'%(k+q*50000) for q in range(6))
for tgt in ['r5x','r3x','u2']:
  for a,s in anch.items():
    for cn,cf in (('a',c1),('b',c2),('c',c3)):
      k+=10
      assert T.count(s)==1,a
      open('v2/%s_%s_%s.c'%(tgt,a,cn),'w',newline='\n').write(T.replace(s,s+' if (%s) goto %s;'%(cf(k),tgt)))
