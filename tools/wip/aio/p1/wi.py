"""wi.py TAG b=k ...: r4sim what-if; prints head order subseq vs REF4 + inversion-ish dist"""
import sys,nm,r4sim
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%sys.argv[1])
def run(ov):
    o=r4sim.sim(pre,g,ov)
    s=[h for h in o if h in set(nm.REF4)]
    return o,s
def dist(s):
    # number of positions differing
    return sum(a!=b for a,b in zip(s,nm.REF4))
if __name__=='__main__':
    ov=dict((int(a),int(b)) for a,b in (x.split('=') for x in sys.argv[2:]))
    o,s=run(ov)
    print('real ok',r4sim.sim(pre,g,{})==first)
    print(dist(s),' '.join(nm.N.get(h,str(h)) for h in s))
