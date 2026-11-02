import sys
S=open(sys.argv[1]).read(); V={}
def r(n,a,b):
    if S.count(a)==1: V[n]=S.replace(a,b)
r('p0mv','if (arg == dummy || ({JMP(p0); 0;}))','if (({JMP(p0); 0;}) || arg == dummy)')
r('c11mv','JMP(c11); break;','break; JMP(c11);')
r('c11b','AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef); }\n\t\t\t\tJMP(c11);','AT(c8) { JMP(c11); clientReadBlocks(arg, start, count); JMP(p1,cdef); }\n\t\t\t\t')
r('dspmv','{ AT(s5)JMP(dsp);  {','{ AT(s5) {')
r('i1mv','AT(cdef)JMP(i1);  if','AT(cdef) if')
r('c3a','AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }','AT(c3)  { JMP(hdd4,s5); clientKeys(); JMP(hdd5); }')
r('c3b','AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }','AT(c3)  { JMP(s5,hdd4,hdd5); clientKeys(); }')
r('c3c','AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }','AT(c3)  { JMP(hdd4,hdd5,s5); clientKeys(); }')
r('u2','{ AT(u2) client_usage(2, NULL); }','{ client_usage(2, NULL); }')
r('t4','AT(t4)  if','if')
r('t5','AT(t5)  if','if')
for k,v in V.items(): open(sys.argv[2]+"/%s.c"%k,'w',newline='\n').write(v)
