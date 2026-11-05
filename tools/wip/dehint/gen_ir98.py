"""findAnchor no hints: gen_ir96's h/i shape (`ok0` cleared, S1 test, `if (!ok1) I1`, S0): CFG exact, both V1s copies.  dom3 must not thread (4,5)(5,6):
that needs its second edge to start a thread of its own (V1 -> T), as in clr.  Clear form x S1 test x where."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
C_OUT = {
    'h': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n',
    'i': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
    'j': 'if (ok1 && ok0 && v0 < v1) ok0 = 0;\n',
    'k': 'if (ok1 && v0 < v1) ok0 = 0;\n',
    'l': 'if (ok1) { if (v0 < v1) ok0 = 0; }\n',
    'm': 'if (v0 < v1 && ok1) ok0 = 0;\n',
}
C_IN = {
    'p': 'if (ok0 && v0 < v1) ok0 = 0;\n',
    'q': 'if (ok0) { if (v0 < v1) ok0 = 0; }\n',
    'r': 'if (v0 < v1) ok0 = 0;\n',
}
T = {
    'a': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'b': f'if (!ok0 && ok1) {{ {S1} }}\n',
    'c': f'if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'd': f'if (ok1) {{ if (!ok0) {{ {S1} }} }}\n',
    'e': f'if (!(ok0 || !ok1)) {{ {S1} }}\n',
}
INV = {'n': f'if (!ok1) {{ {I1} }}\n', 'o': f'if (!ok1) {{ {I1} }}\n'}
END = {'s': SEL0, 'r': f'if (!ok0) return 0;\n {S0}', 'e': f'if (ok0) {{ {S0} }} else return 0;\n'}
TAILS = {}
for t, tt in T.items():
    for e, ee in END.items():
        for c, cc in C_OUT.items():
            TAILS[c + t + e] = f'if (ok1) {V1} {cc} {tt} {INV["n"]} {ee}'
        for c, cc in C_IN.items():
            TAILS[c + t + e] = f'if (ok1) {{ {V1} {cc} }} {tt} {INV["n"]} {ee}'
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
AXES = [AX]
