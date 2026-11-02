import re,os,itertools
s=open('h0.c').read()
m0=s.index('int mode_client(')
os.makedirs('g4',exist_ok=True)
I=['if (__builtin_constant_p(block + 77)) goto einv_i;','if (__builtin_constant_p(block+9)) goto eout_i;','if (__builtin_constant_p(block+5)) goto einv_i;']
for x in I: assert x in s
ats=list(re.finditer(r'AT\((\w+)\)',s[m0:]))
b=m0+ats[1].end()
for k in (1,2,4):
 for inv in (0,1):
  for bits in itertools.product((0,1),repeat=3):
    c=' && '.join('__builtin_constant_p(argc+%d)'%(7000+j) for j in range(k))
    add=' if (%s) goto efail_i;'%c
    if inv: add+=' if (__builtin_constant_p(argc+7100)) goto einv_i;'
    t=s[:b]+add+s[b:]
    for x,bt in zip(I,bits):
        if bt: t=t.replace(x,'')
    open('g4/k%di%d_%d%d%d.c'%((k,inv)+bits),'w',newline='\n').write(t)
