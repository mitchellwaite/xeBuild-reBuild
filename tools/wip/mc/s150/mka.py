# dead computations freed by early DCE: refill the SSA name free list so ch2's loop PHI gets a low version again
s=open('r1.c',newline='').read()
a='int kk = __builtin_constant_p(argc);'; assert s.count(a)==1
for n in (1,2,3,5,8,12,16,24,32,48,64,96,128,192,256,384):
    d=' '.join('int zd%d = argc + %d; (void)zd%d;'%(k,k+1,k) for k in range(n))
    open('h%d.c'%n,'w',newline='\n').write(s.replace(a,a+' '+d))
