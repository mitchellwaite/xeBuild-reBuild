# case 4: asm goto only on the sendAvatarData arm (hdd4's jmp goes straight to dtg); c8 tail gets stale frequency so c9's label isn't aligned
import re
s=open('t1.c',newline='').read()
a='s4: { sendAvatarData(arg, cinfo->kernel); }'; assert s.count(a)==1
ls=s.split('\n')
i=[n for n,x in enumerate(ls) if x.strip()=='case 4:'][-1]
j=[n for n in range(i,i+8) if re.match(r'\s*__asm__ goto \("" : : "i"\(\d+\) : : dsp\); break;',ls[n])][0]
asm=ls[j].strip().replace(' break;','')
ls[j]='\t\t\t\tbreak;'
s2='\n'.join(ls).replace(a,'s4: { sendAvatarData(arg, cinfo->kernel); %s }'%asm)
open('aa0.c','w',newline='\n').write(s2)
c='{ __asm__ goto ("" :::: S761, hdd4); JMP(c11); break; }'; assert s2.count(c)==1
h='AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef); }'; assert s2.count(h)==1
def cps(k): return ' && '.join('__builtin_constant_p(i + %d)'%(18000+j) for j in range(k))
for k in (1,2,3,4):
    x=s2.replace(c,'{ __asm__ goto ("" :::: S761, hdd4); c8t: JMP(c11); break; }').replace(h,'AT(c8) if (%s) goto c8t; { clientReadBlocks(arg, start, count); JMP(p1,cdef); }'%cps(k))
    open('aa%d.c'%k,'w',newline='\n').write(x)
