import re,os
s=open('h0.c').read()
m0=s.index('int mode_client(')
os.makedirs('g',exist_ok=True)
n=0
def w(t,tag):
    global n
    open('g/%s.c'%tag,'w',newline='\n').write(t); n+=1
# a: append eout_i to each JMP in main
for i,mm in enumerate(re.finditer(r'JMP\(([^)]*)\)',s[m0:])):
    a=m0+mm.start(); b=m0+mm.end()
    w(s[:a]+'JMP(%s,eout_i)'%mm.group(1)+s[b:],'a%02d'%i)
# b: standalone JMP(eout_i) after each AT(x) label in main (not eout_i itself)
for i,mm in enumerate(re.finditer(r'AT\((\w+)\)',s[m0:])):
    b=m0+mm.end()
    w(s[:b]+' JMP(eout_i);'+s[b:],'b%02d'%i)
    w(s[:b]+' if (__builtin_constant_p(argc+%d)) goto eout_i;'%(7000+i)+s[b:],'c%02d'%i)
print(n)
