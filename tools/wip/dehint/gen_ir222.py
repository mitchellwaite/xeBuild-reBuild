"""findAnchor attempt 16: the reference's threads come from the clearing test at the join of V1 and I1 (its true edge inflated by vrp1's thread
and MAX in merge_blocks).  xanr has those but I1 is before S1.  Write I1 after S1 by goto: chain V1, S1, I1, S0 with the same CFG as xanr."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
CL = {
    'a': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
    'b': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n',
    'c': 'if (ok0) { if (ok1) { if (v0 < v1) ok0 = 0; } }\n',
    'd': 'if (ok1) { if (ok0) { if (v0 < v1) ok0 = 0; } }\n',
    'f': 'if (ok1) { if (ok0 && v0 < v1) ok0 = 0; }\n',
    'g': 'if (ok0) { if (ok1 && v0 < v1) ok0 = 0; }\n',
    'i': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'l': 'if (ok0 && ok1) { if (v0 >= v1) ok1 = 0; else ok0 = 0; }\n',
}
ARM = {
    'x': f'if (ok1) {V1} else goto inv1;\n check:\n',
    'y': f'if (!ok1) goto inv1;\n {V1} check:\n',
}
# everything after the clear, S1 before I1 before S0
TL = {
    'n': lambda: f'if (!ok0) {{ if (ok1) {{ {S1} }} return 0;\n }}\n goto sel0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'm': lambda: f'if (!ok0 && ok1) {{ {S1} }}\n if (!ok0) return 0;\n goto sel0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'o': lambda: f'if (ok0) goto sel0;\n if (ok1) {{ {S1} }}\n return 0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'p': lambda: f'if (ok1 && !ok0) {{ {S1} }}\n if (ok0) goto sel0;\n return 0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'q': lambda: f'if (!ok0 && ok1) {{ {S1} }}\n if (!ok0) return 0;\n sel0:\n {S0} inv1:\n {I1} goto check;\n',
}
AX = []
for ak, arm in ARM.items():
    for ck, c in CL.items():
        for tk, t in TL.items():
            AX.append((ak + ck + tk, [(OLD, HEADV0 + arm + c + t() + '}\n')]))
TY = [('uu', []), ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')]), ('ui', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0;\n	int ok1;\n')])]
AXES = [AX, TY]
