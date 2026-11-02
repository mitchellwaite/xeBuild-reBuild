# no asm in case 6 (jump table entry must be dtg): raise ndl's frequency with dead constant_p feeds so 161 still pops before 159 in round 2
s=open('b1.c',newline='').read()
a='if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;'; assert s.count(a)==1
b='if (__builtin_constant_p(mode + 130)) goto dtg;'; assert s.count(b)==1
c='dsp: cinfo = netGetInfo();'; assert s.count(c)==1
def cps(v,base,k): return ' && '.join('__builtin_constant_p(%s + %d)'%(v,base+j) for j in range(k))
for k in (3,4,5,6,7):
    open('f%d.c'%k,'w',newline='\n').write(s.replace(a,a+' if (%s) goto ndl;'%cps('i',12000,k)))
for k in (1,2,3):
    open('g%d.c'%k,'w',newline='\n').write(s.replace(b,b+' if (%s) goto ndl;'%cps('mode',12000,k)))
    open('e%d.c'%k,'w',newline='\n').write(s.replace(c,'if (%s) goto ndl; '%cps('mode',12000,k)+c))
