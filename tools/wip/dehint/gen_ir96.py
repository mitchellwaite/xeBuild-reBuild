"""findAnchor no hints: valid log and invalid log in separate tests, with the selection of 1 between them, so S1 is expanded before I1
and the test after the selection is a real join until dom3 (`_a & _b` false edges give VRP nothing)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
FV = {'v': f'if (ok1) {V1}'}
SEL = {
    'a': f'if (ok1 && (!ok0 || v0 < v1)) {{ {S1} }}\n',
    'b': f'if (ok1) {{ if (!ok0 || v0 < v1) {{ {S1} }} }}\n',
    'c': f'if (ok1 && !ok0) {{ {S1} }}\n if (ok1 && v0 < v1) {{ {S1} }}\n',
    'd': f'if (!ok0 || v0 < v1) {{ if (ok1) {{ {S1} }} }}\n',
    'e': f'if (ok1) {{ if (!ok0) {{ {S1} }} if (v0 < v1) {{ {S1} }} }}\n',
    'f': f'if (ok1 && (v0 < v1 || !ok0)) {{ {S1} }}\n',
    'g': f'if (ok1 && !(ok0 && v0 >= v1)) {{ {S1} }}\n',
    'h': f'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n if (ok1 && !ok0) {{ {S1} }}\n',
    'i': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; }}\n if (!ok0 && ok1) {{ {S1} }}\n',
    'j': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; }}\n if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'k': f'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'l': f'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n if (ok1) {{ if (!ok0) {{ {S1} }} }}\n',
    'm': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; }}\n if (ok1) {{ if (!ok0) {{ {S1} }} }}\n',
}
INV = {'n': f'if (!ok1) {{ {I1} }}\n', 'z': f'if (ok1 == 0) {{ {I1} }}\n'}
END = {'s': SEL0, 'r': f'if (!ok0) return 0;\n {S0}'}
AX = [(a + b + c, [(OLD, HEADV0 + FV['v'] + SEL[a] + INV[b] + END[c] + '}\n')]) for a in SEL for b in INV for c in END]
AXES = [AX]
