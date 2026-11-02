import re,sys
src=open('b0.c').read()
T="c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail".split()
# sites: each asm goto ("" :::: LIST) or JMP(LIST) occurrence in function body (after line 600)
start=src.index('\n',sum(len(l)+1 for l in src.split('\n')[:640]))
pat=re.compile(r'(__asm__ goto ?\("" :::: |JMP\()([a-z0-9_, ]+)\)')
sites=[m for m in pat.finditer(src) if m.start()>start]
n=0
for si,m in enumerate(sites):
    labs=[x.strip() for x in m.group(2).split(',')]
    for t in T:
        if t in labs: continue
        new=src[:m.end(2)]+', '+t+src[m.end(2):]
        open('v/s%02d_%s.c'%(si,t),'w',newline='\n').write(new); n+=1
print(len(sites),n)
