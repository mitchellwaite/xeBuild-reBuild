import sys,subprocess
L=open('w.c').read().split('\n')
O='(char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'
def bcp(base,n,lab): return '' if n==0 else 'if ('+' && '.join('__builtin_constant_p(i + %d)'%(base+1000*j) for j in range(n))+') goto %s;'%lab
for k55 in (1,):
  for w3 in (0,3,4,5,6):
    for w4 in (2,3,4,5):
      M=list(L); M[592]=' '+bcp(777100,w3,'wb3')+' '+bcp(888100,w4,'wb4')
      M[666]=M[666].replace(O,'(char *)__builtin_constant_p(i + 30) == (char *)1) goto k55l;')
      open('v/g_%d_%d.c'%(w3,w4),'w',newline='\n').write('\n'.join(M))
