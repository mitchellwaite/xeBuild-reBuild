"""findAnchor, no literal asm (attempt 15): gen_ir212 `anr` leaves the chain right (V1 in place, S1, I1, S0) with V0's copy of V1 reaching S0 through the ok0 test.
So the older-block case goes straight to S0: forms of the both-valid test with a goto or S0 in the arm, ok1 no longer cleared."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
C = {
    'a': 'if (ok0 && ok1) { if (v0 >= v1) goto sel0; ok0 = 0; }\n',
    'b': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else goto sel0; }\n',
    'c': 'if (ok1 && ok0) { if (v0 >= v1) goto sel0; ok0 = 0; }\n',
    'd': 'if (ok0) { if (ok1) { if (v0 >= v1) goto sel0; ok0 = 0; } }\n',
    'e': 'if (ok0 && ok1 && v0 >= v1) goto sel0;\n if (ok0 && ok1) ok0 = 0;\n',
    'f': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { S0S } }\n',
    'g': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n if (ok0 && ok1) goto sel0;\n',
}
S = {
    'n': f'if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'm': f'if (!ok0 && ok1) {{ {S1} }}\n',
    'o': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'p': f'if (ok1) {{ if (!ok0) {{ {S1} }} }}\n',
}
E = {
    'r': f'if (!ok1) {{ {I1} }}\n if (!ok0) return 0;\n sel0:\n {S0}',
    's': f'if (!ok1) {{ {I1} }}\n if (ok0) {{ sel0:\n {S0} }}\n return 0;\n',
    't': f'if (ok1 == 0) {{ {I1} }}\n if (ok0 == 0) return 0;\n sel0:\n {S0}',
}
TAILS = {}
for ck, c in C.items():
    for sk, s in S.items():
        for ek, e in E.items():
            TAILS[ck + sk + ek] = f'if (ok1) {V1}' + c.replace('S0S', S0) + s + e
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', []), ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')])]
AXES = [AX, TY]
