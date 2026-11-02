# gz.py BASE PFX BODY : add zd label to every asm-goto list (front 'f' / back 'b'), zd defined after final return
import sys,re
base,pfx=sys.argv[1],sys.argv[2]
body=sys.argv[3] if len(sys.argv)>3 else '__asm__ volatile (""); __builtin_unreachable();'
s=open(base).read()
i=s.find('return 0;',s.find('connect to xbox server'))+len('return 0;')
s=s[:i]+' zd: '+body+s[i:]
sites=[m for m in re.finditer(r'(__asm__ goto \("" :::: )([^)]*)\)',s)]
sites+= [m for m in re.finditer(r'(JMP\()([^)]*)\)',s) if m.group(2)!='...']
n=0
for k,m in enumerate(sites):
    for f in 'fb':
        lab=m.group(2); new=('zd, '+lab) if f=='f' else (lab+', zd')
        t=s[:m.start(2)]+new+s[m.end(2):]
        open('%s_%02d%s.c'%(pfx,k,f),'w',newline='\n').write(t); n+=1
        print('%s_%02d%s'%(pfx,k,f), lab[:20])
