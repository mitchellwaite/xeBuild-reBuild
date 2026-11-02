import sys,os
TAG=sys.argv[1]
OVS=eval(sys.argv[2]) if len(sys.argv)>2 else [{}]
sys.argv=['ds',TAG]
exec(open('ds.py').read().split('BASEOV=')[0])
heads=list(first)
keys=[0,-1,-2,-3,-4,-8,-11,-15,-19,-30,-37,-38,-40,-57,-73,-76,-79]
for ov in OVS:
    print(ov,'base',score(ov,[])[:2],flush=True)
    S=[]
    for b in heads:
        for key in keys:
            for pos in (0,99):
                s=score(ov,[(b,pos,key)])[:2]
                S.append((s,(b,pos,key)))
    S.sort(key=lambda x:x[0])
    print(ov,'single',S[:8],flush=True)
    top=[x[1] for x in S[:25]]
    P=[]
    for a in top:
        for b in heads:
            for key in keys:
                for pos in (0,99):
                    s=score(ov,[a,(b,pos,key)])[:2]
                    if s[0]<=S[0][0][0]: P.append((s,a,(b,pos,key)))
    P.sort(key=lambda x:x[0])
    print(ov,'pair',P[:12],flush=True)
