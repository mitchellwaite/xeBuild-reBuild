"""findAnchor no hints, gen_ir96 hnr (CFG exact, S1 before I1, both V1s copies).  dom3's (4,5)(5,6)(6,9) must be cancelled, as in clr: that needs 6's false edge straight
to the PHI block, so no `_4 = ok0 == 0` from PRE on the way: spell the first test so `ok0 == 0` is already available, or the S1 test on `ok0 != 0`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
C = {
    'c1': 'if (!ok0 || !ok1) ; else if (v0 < v1) ok0 = 0;\n',
    'c2': 'if (!ok0 || !ok1 || v0 >= v1) ; else ok0 = 0;\n',
    'c3': 'if (!(!ok0 || !ok1) && v0 < v1) ok0 = 0;\n',
    'c4': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n',
    'c5': 'if (ok0 != 0 && ok1 != 0) { if (v0 < v1) ok0 = 0; }\n',
    'c6': 'if (ok1 && ok0 && v0 < v1) ok0 = 0;\n',
    'c7': 'if (ok1) { if (ok0 && v0 < v1) ok0 = 0; }\n',
    'c8': 'if (ok1) { if (ok0) { if (v0 < v1) ok0 = 0; } }\n',
    'c9': 'if (ok1 && !(!ok0 || v0 >= v1)) ok0 = 0;\n',
}
T = {
    'a': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'b': f'if (ok0 == 0 && ok1 != 0) {{ {S1} }}\n',
    'c': f'if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'd': f'if (!(ok0 != 0 || ok1 == 0)) {{ {S1} }}\n',
    'e': f'if (ok0) ; else if (ok1) {{ {S1} }}\n',
    'f': f'if (ok1) {{ if (ok0) ; else {{ {S1} }} }}\n',
    'g': f'if (ok0 || !ok1) ; else {{ {S1} }}\n',
}
INV = {'n': f'if (!ok1) {{ {I1} }}\n', 'o': f'if (ok1) ; else {{ {I1} }}\n'}
END = {'r': f'if (!ok0) return 0;\n {S0}', 's': SEL0}
TAILS = {}
for c, cc in C.items():
    for t, tt in T.items():
        for i, ii in INV.items():
            for e, ee in END.items():
                TAILS[c + t + i + e] = f'if (ok1) {V1} {cc} {tt} {ii} {ee}'
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
AXES = [AX]
