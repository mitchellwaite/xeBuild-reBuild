import re,os,itertools
s=open('h0.c').read()
m0=s.index('int mode_client(')
os.makedirs('g5',exist_ok=True)
ats=list(re.finditer(r'AT\((\w+)\)',s[m0:]))
L=['efail_i','eerase_i','esucc_i','eout_i','einv_i']
n=0
for combo in itertools.combinations_with_replacement(L,2):
  for sites in ((1,1),(1,13),(13,1)):
    t=s
    adds={}
    for j,(lab,si) in enumerate(zip(combo,sites)):
        adds.setdefault(si,'')
        adds[si]+=' if (__builtin_constant_p(argc+%d)) goto %s;'%(7200+n*3+j,lab)
    for si in sorted(adds,reverse=True):
        b=m0+ats[si].end(); t=t[:b]+adds[si]+t[b:]
    open('g5/%s_%s_%d%d.c'%(combo[0][:-2],combo[1][:-2],sites[0],sites[1]),'w',newline='\n').write(t); n+=1
print(n)
