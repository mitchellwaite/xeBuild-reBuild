"""Attempt 54: loadBl24's one-call `||` body (a50_bl24 'or') for lab_none, with loadBlFiles' uses
in several forms; console without its precheck and cold label.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a54_or.py [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub
import a50_bl24 as B

BASE = H.BASE
def nolab(t):
    t = sub(t, *H.NONE); t = sub(t, *H.NONE2)
    return t
def orb(t):
    return sub(t, B.OLD, B.BODIES['or'])
V = {
    'or_none': lambda t: nolab(orb(t)),
    'or_lab': lambda t: orb(t),
    'src_none': lambda t: nolab(t),
}

CON = '\t\t\t\tif (xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);\n'
CONS = {
    'c_and': '\t\t\t\tif (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))\n\t\t\t\t\tr = defaultBl60(e);\n',
    'c_nest': '\t\t\t\tif (xb.glitch2mfg) {\n\t\t\t\t\tif (loadBaseFile(e->name, e) || e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t}\n',
    'c_two': '\t\t\t\tif (xb.glitch2mfg) {\n\t\t\t\t\tif (loadBaseFile(e->name, e))\n\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t\telse if (e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t}\n',
}
for k, c in CONS.items():
    V[k + '_none'] = lambda t, c=c: nolab(sub(t, CON, c))
    V[k + '_lab'] = lambda t, c=c: sub(t, CON, c)
