"""Attempt 50: loadBl24 in its `||` form (frees lab_none in loadConsoleBlFiles, a50_bl24.py) with
loadBlFiles' first case-24 arm written out (two calls) instead of calling it.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_orc.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF
import a50_bl24 as B

BASE = H.BASE
A1 = '\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);\n'
W1 = ('\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg) {\n\t\t\t\t\tif (loadBaseFile(e->name, e))\n'
      '\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t\telse if (e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t}\n')
V = {}
for b in ('or', 'and', 'src'):
    for k in ('all', 'none', 'lab', 'pr'):
        def f(t, b=b, p=OFF[k]):
            t = sub(t, B.OLD, B.BODIES[b])
            t = sub(t, A1, W1)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V[b + '_' + k] = f
