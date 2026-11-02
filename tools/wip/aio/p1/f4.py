"""f4.py OUT opts: from n1.c; opts: ai = guard + always_inline copy of optIniBool; ai0 = no guard, ai copy; early=..."""
import re,sys
t=open(__file__.replace('f4.py','n1.c'),newline='').read()
opts=set(sys.argv[2].split(','))
i=t.index('_Bool optIniBool('); j=t.index('int optIniInt(')
b=t[i:j]
if 'ai' in opts or 'ai0' in opts:
    bb=b.replace('_Bool optIniBool(','static inline __attribute__((always_inline)) _Bool optIniBoolI(')
    k=t.index('/* optIniBool\'s body in the caller')
    t=t[:k]+bb+t[k:]
    gu='if (!(xb.bootFlags & (set))) ' if 'ai' in opts else ''
    t=t.replace('#define OPT(name, set, clear) if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0)','#define OPT(name, set, clear) '+gu+'optIniBoolI(name, set, clear, 0)')
open(sys.argv[1],'w',newline='\n').write(t)
