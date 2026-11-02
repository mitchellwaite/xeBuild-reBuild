# subsets of distinct dsp asm gotos
import re, itertools
s=open('l1.c',newline='').read()
pat=r'__asm__ goto \("" :::: dsp\);'
sites=[m.span() for m in re.finditer(pat,s)]
print(len(sites), [s.count('\n',0,a)+1 for a,b in sites])
def mk(sub):
    out=s; 
    for k in sorted(sub,reverse=True):
        a,b=sites[k]; out=out[:a]+'__asm__ goto ("" : : "i"(%d) : : dsp);'%(101+k)+out[b:]
    return out
for r in (1,2):
    for sub in itertools.combinations(range(len(sites)),r):
        open('../sub/m'+'_'.join(map(str,sub))+'.c','w',newline='\n').write(mk(sub))
