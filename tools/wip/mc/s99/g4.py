import sys,subprocess
s=open('J1.c').read()
FER=r'log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);'
TOP=r'if (__builtin_constant_p(block + 79) && __builtin_constant_p(block + 80)) goto efail;'
LOOPF=r'if (__builtin_constant_p(block + 910)) goto efail;'
LOOPS=r'if (__builtin_constant_p(block + 910)) goto esucc;'
i=s.rfind(FER)
def w(n,t): open(n+'.c','w',newline='\n').write(t)
# efail loop on asm-volatile split part before printf (loop excluded from printf)
base=s[:i]+'FERX'+s[i+len(FER):]
base=base.replace('FERX '+LOOPF,'FERX',1)
assert 'FERX' in base and base.count(LOOPF)==0
V={
 'm01':'{ fq: __asm__ volatile(""); if (__builtin_constant_p(block + 910)) goto fq; } '+FER,
 'm02':FER+' { fq: __asm__ volatile(""); if (__builtin_constant_p(block + 910)) goto fq; }',
 'm03':'{ fq: __asm__ (""); if (__builtin_constant_p(block + 910)) goto fq; } '+FER,
 'm04':FER+' { fq: __asm__ (""); if (__builtin_constant_p(block + 910)) goto fq; }',
 'm05':'{ fq: __asm__ volatile(""); if (__builtin_constant_p(block + 910)) goto efail; } '+FER,
}
for k,v in V.items():
  t=base.replace('FERX',v); w(k,t); w(k+'n',t.replace(TOP,'',1))
