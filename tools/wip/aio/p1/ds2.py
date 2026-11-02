import sys,nm,time
sys.argv=['ds','n8c'] if len(sys.argv)<2 else sys.argv
exec(open('ds.py').read().split('BASEOV=')[0])
heads=list(first)
keys=[0,-1,-2,-3,-4,-8,-11,-15,-19,-30,-37,-38,-40,-69,-73,-76,-79]
ovs=[{259:-37,27:-11},{259:-37,27:-10},{259:-37,27:-9},{259:-37,229:-15},{259:-37,229:-16},{259:-38,27:-11},{259:-38,229:-16}]
for ov in ovs:
    S=[]
    for b in heads:
        for key in keys:
            for pos in (0,1,2,99):
                s=score(ov,[(b,pos,key)])[:2]
                S.append((s,(b,pos,key)))
    S.sort()
    print(ov,'single',S[:6],flush=True)
    top=[x[1] for x in S[:40]]
    P=[]
    for a in top:
        for b in heads:
            for key in keys:
                for pos in (0,99):
                    s=score(ov,[a,(b,pos,key)])[:2]
                    P.append((s,a,(b,pos,key)))
    P.sort()
    print(ov,'pair',P[:8],flush=True)
