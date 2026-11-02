import sys,os
S=open(sys.argv[1]).read(); V={}
def r(n,a,b):
    if S.count(a)!=1: return
    V[n]=S.replace(a,b)
r('m_c9','AT(c9)JMP(s5);  { clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }','AT(c9) { clientWriteBlocks(arg, start); JMP(s5,hdd4,hdd5); }')
r('m_c10','AT(c10)JMP(c10);  clientEraseBlockI(arg);','AT(c10) clientEraseBlockI(arg); JMP(c10);')
r('m_c10b','AT(c10)JMP(c10);  clientEraseBlockI(arg);','AT(c10) clientEraseBlockI(arg);')
r('m_s5','{ AT(s5)JMP(dsp);  { JMP(s4,c12); sendCompatData(arg); } }','{ AT(s5) { JMP(dsp,s4,c12); sendCompatData(arg); } }')
r('m_s5b','{ AT(s5)JMP(dsp);  { JMP(s4,c12); sendCompatData(arg); } }','{ AT(s5) { sendCompatData(arg); JMP(dsp,s4,c12); } }')
r('m_s5c','{ AT(s5)JMP(dsp);  { JMP(s4,c12); sendCompatData(arg); } }','{ AT(s5) { JMP(dsp,s4); sendCompatData(arg); } }')
r('m_c3','AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }','AT(c3)  { clientKeys(); JMP(hdd4,s5,hdd5); }')
r('m_c8','AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef); }\n\t\t\t\tJMP(c11); break;','AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef,c11); }\n\t\t\t\tbreak;')
r('m_cdef','AT(cdef)JMP(i1);  if','AT(cdef) if')
r('m_c12','if (arg == dummy || ({JMP(p0); 0;}))','if (arg == dummy)')
for k,v in V.items(): open(sys.argv[2]+"/%s.c"%k,'w',newline='\n').write(v)
