# distinct empty asm gotos (immediate input) so identical "asm goto dsp; jmp dtg" tails aren't cross-jumped into jmp-to-jmp
import re
s=open('l1.c',newline='').read()
n=[100]
def rep(m):
    n[0]+=1; return '__asm__ goto ("" : : "i"(%d) : : dsp);'%n[0]
a=re.sub(r'__asm__ goto \("" :::: dsp\);',rep,s); print(n[0]-100)
open('t1.c','w',newline='\n').write(a)
a2=re.sub(r'JMP\(dsp\);',rep,a); print(n[0]-100)
open('t2.c','w',newline='\n').write(a2)
