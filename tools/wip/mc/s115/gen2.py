import re
src=open('b0.c').read()
T="c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail".split()
lines=src.split('\n')
off=sum(len(l)+1 for l in lines[:736])
end=sum(len(l)+1 for l in lines[:792])
pos=[m.start() for m in re.finditer(r'break;',src) if off<m.start()<end]
pos+=[m.end() for m in re.finditer(r'AT\([a-z0-9]+\)',src) if off<m.start()<end]
n=0
for si,p in enumerate(pos):
    for t in T:
        open('w/n%02d_%s.c'%(si,t),'w',newline='\n').write(src[:p]+'JMP(%s); '%t+src[p:]); n+=1
print(len(pos),n)
