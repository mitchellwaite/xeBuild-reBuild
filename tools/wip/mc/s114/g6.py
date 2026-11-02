import sys
b=open('b0.c').read(); a=open('a_c6_c11.c').read()
k4=a.replace('__asm__ goto ("" :::: c11); break;','break;',1)  # k4 = c11 4 conj
OLD='case 6:\n\t\t\t\tbreak;'
for base,bn in ((b,'b'),(k4,'k')):
  for lab in ('c11','c3','c9','c7','cdef','c1','c2','c10','c12'):
    for n in range(1,7):
      cond=' && '.join('__builtin_constant_p(mode + %d)'%(777000+lab.__hash__()%1000*7+i*13) for i in range(n))
      t=base.replace(OLD,'case 6:\n\t\t\t\tif (%s) goto %s; break;'%(cond,lab),1)
      assert t!=base
      open('v/%s_%s_%d.c'%(bn,lab,n),'w',newline='\n').write(t)
