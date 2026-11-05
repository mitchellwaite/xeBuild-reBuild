"""findAnchor no hints: a second copy of S1 written in the valid arm, so its string is expanded before I1, and RTL/tail merge joins the copies.
Tail: gen_ir93's flag-clearing forms or nested forms."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
CL = {
    'a': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'b': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n',
    'c': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
    'd': 'if (ok1 && v0 < v1) ok0 = 0;\n',
    'e': 'if (ok1) { if (v0 < v1) ok0 = 0; }\n',
    'f': '',
}
TAILS = {
    # valid arm has its own S1 when 0 is bad
    'F1': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} }} else {{ {I1} if (!ok0) return 0; }}\n if (ok1 && v0 < v1) {{ {S1} }} {S0}',
    'F2': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} }} else {{ {I1} if (!ok0) return 0; }}\n if (ok1) {{ if (v0 < v1) {{ {S1} }} }} {S0}',
    'F3': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} if (v0 < v1) {{ {S1} }} }} else {{ {I1} if (!ok0) return 0; }}\n {S0}',
    'F3a': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} if (v0 < v1) {{ {S1} }} {S0} }} {I1} if (!ok0) return 0;\n {S0}',
    'F3b': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} if (v0 < v1) {{ {S1} }} }} else {{ {I1} }}\n {SEL0}',
    'F3c': f'if (ok1) {{ {V1} if (!ok0 || v0 < v1) {{ {S1} }} }} else {{ {I1} }}\n {SEL0}',
    'F3d': f'if (ok1) {{ {V1} if (ok0) {{ if (v0 < v1) {{ {S1} }} }} else {{ {S1} }} }} else {{ {I1} }}\n {SEL0}',
    'F3e': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} else if (v0 < v1) {{ {S1} }} }} else {{ {I1} }}\n {SEL0}',
    'F3f': f'if (ok1) {{ {V1} if (ok0) {{ if (v0 < v1) {{ {S1} }} {S0} }} {S1} }} {I1} {SEL0}',
    'F3g': f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} if (v0 < v1) {{ {S1} }} {S0} }} {I1} {SEL0}',
}
for k, c in CL.items():
    TAILS['F7' + k] = f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} }} else {{ {I1} }}\n {c} if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n'
    TAILS['F8' + k] = f'if (ok1) {{ {V1} if (!ok0) {{ {S1} }} {c} }} else {{ {I1} }}\n if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n'
    TAILS['F9' + k] = f'if (ok1) {V1} else {{ {I1} }}\n if (!ok0 && ok1) {{ {S1} }}\n {c} if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n'
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
AXES = [AX]
