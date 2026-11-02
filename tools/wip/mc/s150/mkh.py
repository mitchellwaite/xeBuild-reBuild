# two more zero-byte dummies (key -2) from the erase head: cold folded arm for the asm goto (no flow), frequency from dead feeds + dead return
s=open('w3fr.c',newline='').read().split('\n')
i=[n for n,x in enumerate(s) if 'uint32_t block = myatoh32' in x][-1]
iv=[n for n,x in enumerate(s) if 'einv: __attribute__((cold));' in x][-1]
def cp(a): return '__builtin_constant_p(block + %d)'%a
def arm(tag,l,a): return 'if (!%s) { %s: __attribute__((cold)); __asm__ goto ("" :::: %s); } '%(cp(a),tag,l)
def feed(l,k,a,bk): return 'if (%s) goto %s; %s:; '%(' && '.join(cp(a+j) for j in range(k)),l,bk)
def dum(l,clob,a,bk): return 'if (0) { %s: asm volatile("" : : : %s); if (%s) goto %s; __builtin_unreachable(); } '%(l,clob,cp(a),bk)
for k in (1,2,3):
  for n,order in (('a',0),('b',1)):
    x=list(s)
    body=arm('ae1','da',930)+feed('da',k,931,'dab')+arm('ae2','db',940)+feed('db',k,941,'dbb') if order==0 else feed('da',k,931,'dab')+feed('db',k,941,'dbb')+arm('ae1','da',930)+arm('ae2','db',940)
    x.insert(i+1,'\t'+body)
    x[iv+1]=x[iv+1].replace('{ if (0) { dy:','{ '+dum('da','"cc", "memory"',950,'dab')+dum('db','"fpsr"',951,'dbb')+'if (0) { dy:',1)
    open('z%d%s.c'%(k,n),'w',newline='\n').write('\n'.join(x))
