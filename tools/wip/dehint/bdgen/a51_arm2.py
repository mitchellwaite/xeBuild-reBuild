"""Attempt 51: loadBl24 bodies (a50_bl24.BODIES) crossed with case 24's second arm (written out as src,
or calling loadBl24), the devgl label on/off and console's precheck + cold label on/off.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_arm2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, LAB
import a50_bl24 as B
import a50_arm2 as A

BASE = H.BASE
V = {}
bodies = os.environ.get('A51_B', 'src,or,and,r2,nest,ok1,g0,n2,n3,r3,r4').split(',')
for b in bodies:
    for form in ('w', 'call'):
        for lab in (1, 0):
            for none in (0, 1):
                if form == 'w' and lab == 1 and none == 0 and b == 'src':
                    continue
                def g(t, b=b, form=form, lab=lab, none=none):
                    t = sub(t, B.OLD, B.BODIES[b])
                    if form == 'call':
                        t = A.arm('call', lab)(t)
                    elif not lab:
                        t = sub(t, *LAB)
                    if none:
                        t = sub(t, *H.NONE)
                        t = sub(t, *H.NONE2)
                    return t
                V['%s_%s_%s_%s' % (b, form, 'L' if lab else 'n', 'N' if none else 'k')] = g
