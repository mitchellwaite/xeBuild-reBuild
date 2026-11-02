"""bm.py TAG: multiset of code chunks (split after jmp/ret) ref vs ours"""
import sys,collections,ev
o=ev.os.path.join(ev.ROOT,'build/v/aio_p1',sys.argv[1],'o.o')
def chunks(l):
    r=[];c=[]
    for x in l:
        if ev.NOPS.match(x.split(' @')[0]): continue
        c.append(x)
        if x.startswith('jmp') or x.startswith('ret'):
            r.append(tuple(c));c=[]
    if c:r.append(tuple(c))
    return collections.Counter(r)
A=chunks(ev.funcs(ev.REFO)['_applyIniOptions']);B=chunks(ev.funcs(o)['_applyIniOptions'])
print('ref-only');[print(' ',v,' | '.join(k)[:400]) for k,v in (A-B).items()]
print('ours-only');[print(' ',v,' | '.join(k)[:400]) for k,v in (B-A).items()]
