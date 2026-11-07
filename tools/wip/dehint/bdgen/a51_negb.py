"""Attempt 51: exp_pr as `(int)r < 0` (0/7 at p0, attempt 47) on loadBl24 bodies x case 24's second arm
(written out or calling loadBl24) x devgl label: does any move the no-key log's alignment?
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_negb.py -p 0"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, LAB
import a50_bl24 as B
import a50_arm2 as A

BASE = H.BASE
NEG = ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')
V = {}
for b in os.environ.get('A51_B', 'src,or,r2,g0,n2,ok1').split(','):
    for form in ('w', 'call'):
        for lab in (1, 0):
            def g(t, b=b, form=form, lab=lab):
                t = sub(t, B.OLD, B.BODIES[b])
                if form == 'call':
                    t = A.arm('call', lab)(t)
                elif not lab:
                    t = sub(t, *LAB)
                return sub(t, *NEG)
            V['%s_%s_%s' % (b, form, 'L' if lab else 'n')] = g
