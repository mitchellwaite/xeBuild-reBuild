# efail's trailing jmp in its own block C (zero-byte asm) with a stale nonzero frequency: the -w label's prev block isn't freq 0, so no alignment
s=open('w3fr.c',newline='').read().split('\n')
ie=[n for n,x in enumerate(s) if 'AT(efail)' in x][-1]
er=[n for n,x in enumerate(s) if 'eerase:' in x][-1]
cp=lambda a:'__builtin_constant_p(block + %d)'%a
for k in (1,2,3):
    x=list(s); assert 'JMP(dy); }' in x[ie]
    x[ie]=x[ie].replace('JMP(dy); }','JMP(dy); efcl: asm volatile("" : : "i"(64)); }')
    q=x[er].index('log_printf'); x[er]=x[er][:q]+'if (%s) goto efcl; '%' && '.join(cp(960+j) for j in range(k))+x[er][q:]
    open('l%d.c'%k,'w',newline='\n').write('\n'.join(x))
