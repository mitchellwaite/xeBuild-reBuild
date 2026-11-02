import itertools, random, m, sys
src=open('best_g7b_dup.c').read()
old='JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
labs=['i1','p1','hdd5','hdd4','c10','c9','c1','c7','cdef','s4','s5','c3','c2','c8']
random.seed(int(sys.argv[1]))
best=None
for t in range(int(sys.argv[2])):
    k=random.randint(1,5); sub=random.sample(labs,k)
    new=old+' JMP(%s);'%','.join(sub)
    try: r=m.meas(src.replace(old,new),'sc%s_%d'%(sys.argv[1],t))
    except Exception as e: print('err',sub,e); continue
    inv=[x for x in r['raw'] if False] if 0 else None
    s=str(r); import re; mm=re.search(r"inv (\d+)",s); v=int(mm.group(1)) if mm else 999
    print(v,sub,flush=True)
