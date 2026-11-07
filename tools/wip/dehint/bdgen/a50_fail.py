"""Attempt 50: the could-not-read log shared by both loaders as a helper (returning -1, or void).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_fail.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF, ANCHOR

BASE = H.BASE
LOG = 'log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n'
OLD = '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n'
FN = ('/* the error both loaders end on */\nstatic int notRead(struct fileent *e, uint32_t r)\n{\n\t' + LOG +
      '\treturn -1;\n}\n\n')
FNV = '/* the error both loaders end on */\nstatic void notRead(struct fileent *e, uint32_t r)\n{\n\t' + LOG + '}\n\n'
V = {}
for form in ('ret', 'void'):
    for k in ('all', 'pr', 'lab', 'none', 'bar'):
        def f(t, form=form, p=OFF[k]):
            new = ('\t\tif (r)\n\t\t\treturn notRead(e, r);\n' if form == 'ret' else
                   '\t\tif (r) {\n\t\t\tnotRead(e, r);\n\t\t\treturn -1;\n\t\t}\n')
            t = sub(t, OLD, new, 2)
            t = sub(t, ANCHOR, (FN if form == 'ret' else FNV) + ANCHOR)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V[form + '_' + k] = f
