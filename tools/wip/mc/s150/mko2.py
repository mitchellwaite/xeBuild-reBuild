# c9's last asm block gets a stale nonzero frequency so the c11 label after it isn't aligned
s=open('aa2.c',newline='').read()
import re
m=re.search(r'__asm__ goto \("" : : "i"\(\d+\) : : dsp\); __asm__ goto \("" : : "i"\(\d+\) : : dsp\); (__asm__ goto \("" : : "i"\(\d+\) : : dsp\);) break;\n\t+case 10:',s)
assert m
a='AT(c9)JMP(s5);'; assert s.count(a)==1
def cps(k): return ' && '.join('__builtin_constant_p(i + %d)'%(17000+j) for j in range(k))
for k in (1,2,3,4,5):
    x=s[:m.start(1)]+'c9t: '+s[m.start(1):]
    x=x.replace(a,'AT(c9) if (%s) goto c9t; JMP(s5);'%cps(k))
    open('ab%d.c'%k,'w',newline='\n').write(x)
