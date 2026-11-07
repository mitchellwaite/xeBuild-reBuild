"""Attempt 50: loadXell without its retail test (attempt 49's x1: the test in both callers) on the
landed source, crossed with the barrier and a type == 10 expect (exp_t10), p95/p99.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_x1.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub

BASE = H.BASE
T = '\tif (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)\n\t\treturn 0;\n'
CALL = '\t\t\t\tr = loadXell(e);\n'
CALLX = ('\t\t\t\tif (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)\n\t\t\t\t\tbreak;\n' + CALL)
CALLY = ('\t\t\t\tif (xb.type != BUILD_RETAIL && xb.type <= BUILD_DEVGL16)\n\t\t\t\t\tr = loadXell(e);\n')
T10 = ('} else if (type == 10) {', '} else if (__builtin_expect(type == 10, 0)) {')
V = {}
for form, c in (('brk', CALLX), ('if', CALLY)):
    for bar in (1, 0):
        for t10 in (0, 1):
            def f(t, c=c, bar=bar, t10=t10):
                t = sub(t, T, '')
                t = sub(t, CALL, c, 2)
                if not bar:
                    t = sub(t, *H.BAR)
                if t10:
                    t = sub(t, *T10)
                return t
            V['%s_bar%d_t10%d' % (form, bar, t10)] = f
