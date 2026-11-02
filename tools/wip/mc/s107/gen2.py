import re,os
s=open('h0.c').read()
m0=s.index('int mode_client(')
os.makedirs('g2',exist_ok=True)
E='if (__builtin_constant_p(block+9)) goto eout_i;'
assert E in s
ats=list(re.finditer(r'AT\((\w+)\)',s[m0:]))
for i in [1,2,3,5,8,11,13,16,19]:
  for k in (1,2,3,5):
    for r in (0,1):
      b=m0+ats[i].end()
      c=' && '.join('__builtin_constant_p(argc+%d)'%(7000+i*10+j) for j in range(k))
      t=s[:b]+' if (%s) goto eout_i;'%c+s[b:]
      if r: t=t.replace(E,'')
      open('g2/s%02dk%dr%d.c'%(i,k,r),'w',newline='\n').write(t)
