import re,os,itertools
s=open('h1.c').read()
m0=s.index('int mode_client(')
os.makedirs('g6',exist_ok=True)
ats=list(re.finditer(r'AT\((\w+)\)',s[m0:]))
for lab in ('c10','ecmp_i','enet_i'):
  for si in (1,2,3,8,11,13,16,19):
    for k in (1,2):
      b=m0+ats[si].end()
      add=''.join(' if (__builtin_constant_p(argc+%d)) goto %s;'%(7300+si*5+j,lab) for j in range(k))
      open('g6/%s_%d_%d.c'%(lab,si,k),'w',newline='\n').write(s[:b]+add+s[b:])
