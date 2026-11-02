"""hp.py TAG 'b:+d,..' : hsim prediction of f deltas on TAG history."""
import sys,os
R0=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0,R0+r'\tools\wip\mc\s18'); sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import hsim,pot
R,k=hsim.load(os.path.join(R0,'build','v','mc35','slot_'+sys.argv[1])); f,P=hsim.measured(k)
for a in sys.argv[2:]:
    g=dict(f)
    for x in a.split(','):
        if x: b,d=x.split(':'); g[int(b)]+=int(d)
    o=hsim.sim(R,g,P); print(a,pot.tinv(o),o if isinstance(o,str) else ' '.join(map(str,o))[:200])
