"""Attempt 52, diagnostic only: does an IPA-inlined (not early-inlined) fuse helper whose dev arm is an
early return keep the setne above the dev test?  The helper gets a call so einline refuses it
(growth x (calls + 1) > 14).  Not a candidate: the call is extra code.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_devdiag.py -k <label>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
import a52_dev as D
BASE = H.BASE
CALL = {'imgsz': '\timgSize();\n', 'log': '\tlog_printf(9, "");\n'}
V = {}
for b in ('dret', 'flag', 'd1st'):
    for c in CALL:
        def f(t, b=b, c=c):
            t = D.mk(b, 'if', 'bf', 0)(t)
            return t.replace('static int vfusesUsed(void)\n{\n', 'static int vfusesUsed(void)\n{\n' + CALL[c], 1)
        V['%s_%s' % (b, c)] = f
