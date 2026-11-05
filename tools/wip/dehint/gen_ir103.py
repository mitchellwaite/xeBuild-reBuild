"""findAnchor: clr's CFG with the blocks written in .rdata's order by goto (V1, S1, I1, S0): does chain order alone do it, with threading unchanged?  Would be a candidate at best."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
C = 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n'
TAILS = {
    'g1': f'if (!ok1) goto inv1;\n {V1} check:\n {C} if (ok0) goto sel0;\n if (ok1) {{ {S1} }}\n return 0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'g2': f'if (ok1) {V1} else goto inv1;\n check:\n {C} if (ok0) goto sel0;\n if (ok1) {{ {S1} }}\n return 0;\n inv1:\n {I1} goto check;\n sel0:\n {S0}',
    'g3': f'if (!ok1) {{ inv: {I1} }}\n',
}
del TAILS['g3']
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
AXES = [AX]
