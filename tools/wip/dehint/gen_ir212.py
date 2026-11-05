"""findAnchor, no literal asm (attempt 15): gen_ir211's S1-before-I1 with the join after the selection testing ok0's flag FIRST, so the ok1-false path's thread
stops there at dom2 (as in clr), and V1's false edge can start a thread of its own at dom3, which is what cancels I0's joiner thread and leaves V1 in place."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
C = {
    'a': 'use1 = ok1; if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else use1 = 0; }\n',
    'b': 'use1 = ok1; if (ok0) { if (ok1) { if (v0 < v1) ok0 = 0; else use1 = 0; } }\n',
    'c': 'use1 = ok1; if (ok1 && ok0) { if (v0 < v1) ok0 = 0; else use1 = 0; }\n',
    'd': 'if (ok0 && ok1) { if (v0 < v1) use0 = 0; else use1 = 0; }\n',
    'e': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
}
PRE = {'a': '', 'b': '', 'c': '', 'd': 'use0 = ok0; use1 = ok1;\n', 'e': ''}
Z = {'a': 'ok0', 'b': 'ok0', 'c': 'ok0', 'd': 'use0', 'e': 'ok0'}
S = {
    'n': lambda z, u: f'if (!{z}) {{ if ({u}) {{ {S1} }} }}\n',
    'm': lambda z, u: f'if (!{z} && {u}) {{ {S1} }}\n',
    'e': lambda z, u: f'if ({z}) {{ }} else if ({u}) {{ {S1} }}\n',
}
TI = {'n': f'if (!ok1) {{ {I1} }}\n'}
T0 = {'s': lambda z: f'if ({z}) {{ {S0} }}\n return 0;\n', 'r': lambda z: f'if (!{z}) return 0;\n {S0}'}
TAILS = {}
for ck, c in C.items():
    z = Z[ck]
    u = 'ok1' if ck == 'e' else 'use1'
    for sk, s in S.items():
        for tk, t0 in T0.items():
            TAILS[ck + sk + tk] = f'if (ok1) {V1}' + PRE[ck] + c + s(z, u) + TI['n'] + t0(z)
    # the zero-test-first shape: S0's arm holds I1's test when ok0, so S1 first in the else
    TAILS[ck + 'X'] = f'if (ok1) {V1}' + PRE[ck] + c + f'if ({z}) {{ if (!ok1) {{ {I1} }} {S0} }} else {{ if ({u}) {{ {S1} }} {I1} }}\n return 0;\n'
    TAILS[ck + 'Y'] = f'if (ok1) {V1}' + PRE[ck] + c + f'if (!{z}) {{ if ({u}) {{ {S1} }} {I1} return 0;\n }}\n if (!ok1) {{ {I1} }} {S0}'
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1, use0, use1;\n')]),
      ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1, use0, use1;\n')])]
AXES = [AX, TY]
