"""findAnchor attempt 16: goto form xio (gen_ir222) needs P(v0 < v1) in [53, 89] or P(S1's test) in [38, 62]: live forms for it, no hint."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
CL = {
    'p': 'if (ok0 && ok1) { int newer = v0 < v1; if (newer > 0) ok0 = 0; else ok1 = 0; }\n',
    'q': 'if (ok0 && ok1) { int newer = v0 < v1; if (newer <= 0) ok1 = 0; else ok0 = 0; }\n',
    'r': 'if (ok0 && ok1) { int older = v0 >= v1; if (older > 0) ok1 = 0; else ok0 = 0; }\n',
    's': 'if (ok0 && ok1) { int older = v0 >= v1; if (older <= 0) ok0 = 0; else ok1 = 0; }\n',
    't': 'if (ok0 && ok1) { uint32_t newer = v0 < v1; if (newer == 1) ok0 = 0; else ok1 = 0; }\n',
    'u': 'if (ok0 && ok1) { int newer = v0 < v1; if (newer == 0) ok1 = 0; else ok0 = 0; }\n',
    'v': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'w': 'if (ok0 && ok1) { ok0 = v0 >= v1; ok1 = !ok0; }\n',
    'x': 'if (ok0 && ok1) { if (v0 != v1 && v0 < v1) ok0 = 0; else ok1 = 0; }\n',
}
ARM = {
    'x': f'if (ok1) {V1} else goto inv1;\n check:\n',
    'y': f'if (!ok1) goto inv1;\n {V1} check:\n',
}
T1 = f'if (ok0) goto sel0;\n if (ok1) {{ {S1} }}\n return 0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}'
T2 = f'if (ok0) goto sel0;\n if (!ok1) return 0;\n {S1} inv1:\n {I1} goto check;\n sel0:\n {S0}'
T3 = f'if (!ok0) {{ if (ok1) {{ {S1} }}\n return 0;\n }}\n goto sel0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}'
T4 = f'if (ok1 > 0) {{ {S1} }}\n if (!ok0) return 0;\n goto sel0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}'
T = {'1': T1, '2': T2, '3': T3}
AX = []
for ak, arm in ARM.items():
    for ck, c in CL.items():
        for tk, t in T.items():
            AX.append((ak + ck + tk, [(OLD, HEADV0 + arm + c + t + '}\n')]))
AXES = [AX]
