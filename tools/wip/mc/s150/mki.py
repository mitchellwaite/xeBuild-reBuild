# dummies dw (key -3, from efail) and dx (key -2, from dy) so a nonzero-frequency zero-byte block precedes the -w test
s=open('w3fr.c',newline='').read().split('\n')
ie=[n for n,x in enumerate(s) if 'AT(efail)' in x][-1]
er=[n for n,x in enumerate(s) if 'eerase:' in x][-1]
iv=[n for n,x in enumerate(s) if 'einv: __attribute__((cold));' in x][-1]
ib=[n for n,x in enumerate(s) if 'JMP(efail); if (block < cinfo' in x][-1]
def cp(a): return '__builtin_constant_p(block + %d)'%a
def mk(name, jmp, fw, fx):
    x=list(s)
    assert 'JMP(dy); }' in x[ie]; x[ie]=x[ie].replace('JMP(dy); }',jmp+' }')
    x[ib]=x[ib].replace('JMP(efail);', fw+' JMP(efail);',1)
    k=x[er].index('log_printf'); x[er]=x[er][:k]+fx+' '+x[er][k:]
    dw='if (0) { dw: asm volatile("" : : "i"(61)); if (%s) goto dwb; __builtin_unreachable(); } '%cp(950)
    dx='if (0) { dx: asm volatile("" : : "i"(62)); if (%s) goto dxb; __builtin_unreachable(); } '%cp(951)
    x[iv]=x[iv].replace('{ if (0) { dy: asm volatile(""); ','{ '+dw+dx+'if (0) { dy: asm volatile(""); __asm__ goto ("" :::: dx); ',1)
    open(name+'.c','w',newline='\n').write('\n'.join(x))
FW='if (%s) goto dw; dwb:;'%cp(905)
FW2='if (%s && %s) goto dw; dwb:;'%(cp(905),cp(906))
FX='if (%s) goto dx; dxb:;'%cp(907)
FX2='if (%s && %s) goto dx; dxb:;'%(cp(907),cp(908))
for j,jn in (('JMP(dy,dw);','a'),('JMP(dw,dy);','b'),('JMP(dw); JMP(dy);','c'),('JMP(dy); JMP(dw);','d')):
    for f,fn in ((FW,'1'),(FW2,'2')):
        for g,gn in ((FX,'1'),(FX2,'2')):
            mk('u'+jn+fn+gn,j,f,g)
