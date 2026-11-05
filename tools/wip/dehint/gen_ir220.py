"""findAnchor, no literal asm (attempt 15): V1 and I1 in one test (P(ok1) 50), the selection AFTER their join so that dom2 can't see ok1 there (clr's reason), then S1's test before S0's.
S1 gets ahead of I1 in the chain when it has one predecessor at PRE, a split-edge block placed after V1 (gen_ir218 Dbmr: `Merging blocks 15 and 8`)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
CL = {
    'a': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
    'b': 'if (ok0 && ok1 && v0 < v1) ok0 = 0;\n',
    'c': 'if (ok0) { if (ok1) { if (v0 < v1) ok0 = 0; } }\n',
    'd': 'if (ok1) { if (ok0) { if (v0 < v1) ok0 = 0; } }\n',
    'e': 'if (ok1 && ok0 && v0 < v1) ok0 = 0;\n',
    'f': 'if (ok1) { if (ok0 && v0 < v1) ok0 = 0; }\n',
    'g': 'if (ok0) { if (ok1 && v0 < v1) ok0 = 0; }\n',
    'h': 'if (ok1 && v0 < v1) ok0 = 0;\n',
    'i': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'j': 'if (ok1 && ok0) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'k': 'if (ok1) { if (v0 < v1) ok0 = 0; }\n',
    'l': 'if (ok0 && ok1) { if (v0 >= v1) ok1 = 0; else ok0 = 0; }\n',
}
ST = {
    'm': f'if (!ok0 && ok1) {{ {S1} }}\n',
    'k': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'n': f'if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'p': f'if (ok1) {{ if (!ok0) {{ {S1} }} }}\n',
    'q': f'if (ok1 && (!ok0 || !v0)) {{ {S1} }}\n',
}
del ST['q']
EN = {'r': f'if (!ok0) return 0;\n {S0}', 's': f'if (ok0) {{ {S0} }}\n return 0;\n'}
ARMS = {'x': f'if (ok1) {V1} else {{ {I1} }}\n', 'y': f'if (!ok1) {{ {I1} }} else {V1}'}
TAILS = {}
for ak, arm in ARMS.items():
    for ck, c in CL.items():
        for sk, s in ST.items():
            for ek, e in EN.items():
                TAILS[ak + ck + sk + ek] = arm + c + s + e
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', []), ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')]), ('ui', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0;\n	int ok1;\n')])]
AXES = [AX, TY]
