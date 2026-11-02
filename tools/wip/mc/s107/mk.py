import sys,re
s=open('best.c').read()
a=s.index('static void clientEraseBlockI'); b=s.index('/* the option',a)
fn=s[a:b]; s=s[:a]+s[b:]
body=fn[fn.index('{')+1:fn.rindex('}')]
body=body.replace('uint32_t block = myatoh32(sblock, -1);','uint32_t block = myatoh32(arg, -1);')
body=re.sub(r'\b(eerase|einv|eout|esucc|efail)\b',r'\1_i',body)
s=s.replace('AT(c10) clientEraseBlockI(arg);','AT(c10) {'+body+'}')
open(sys.argv[1],'w').write(s)
