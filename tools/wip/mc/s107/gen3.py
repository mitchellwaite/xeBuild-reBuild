import re,os
s=open('h0.c').read()
m0=s.index('int mode_client(')
os.makedirs('g3',exist_ok=True)
ats=list(re.finditer(r'AT\((\w+)\)',s[m0:]))
for i in [1,2,8,11,13,16,19]:
  for L in ('eerase_i','esucc_i','efail_i','einv_i'):
      b=m0+ats[i].end()
      t=s[:b]+' if (__builtin_constant_p(argc+%d)) goto %s;'%(7000+i,L)+s[b:]
      open('g3/s%02d%s.c'%(i,L[:-2]),'w',newline='\n').write(t)
