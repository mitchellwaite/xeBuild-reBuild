"""findAnchor no hints, second sweep: flag cleared (gen_ir93 clr: code exact, only .rdata) with S1 written before I1, which is what .rdata asks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
CMPS = {
    'c0': 'if (ok0) { if (v0 < v1) ok0 = 0; }\n',
    'c1': 'if (ok0 && v0 < v1) ok0 = 0;\n',
    'c2': 'if (v0 < v1) ok0 = 0;\n',
    'c3': 'if (ok0 && v0 >= v1) ok1 = 0; else ok0 = 0;\n',
    'c4': 'if (ok0) { if (v0 >= v1) ok1 = 0; else ok0 = 0; }\n',
    'c5': 'if (ok0) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'c6': 'if (ok0 && v0 >= v1) ok1 = 0;\n',
    'c7': 'if (ok0) { if (v0 >= v1) ok1 = 0; }\n',
}
TAILS = {}
for k, c in CMPS.items():
    tests = {'n': 'if (!ok0)'} if k in ('c0', 'c1', 'c2') else {'o': 'if (ok1)'}
    for tk, t in tests.items():
        TAILS[k + tk + 'in'] = f'if (ok1) {{ {V1} {c} {t} {{ {S1} }} }} else {{ {I1} }}\n' + SEL0
        TAILS[k + tk + 'ie'] = f'if (ok1) {{ {V1} {c} {t} {{ {S1} }} {SEL0} }} {I1}' + SEL0
        TAILS[k + tk + 'out'] = f'if (ok1) {V1} else {{ {I1} }}\n if (ok1) {{ {c} {t} {{ {S1} }} }}\n' + SEL0
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
AXES = [AX]
