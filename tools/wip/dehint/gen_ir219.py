"""findAnchor, no literal asm (attempt 15): gen_ir218 `Dbmr` (layout and .rdata right, 14 loose: v1/ok0 swap in IRA).  Types of v0, v1, ok0, ok1 and spellings of the tests, for costs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
CL = {'b': 'if (ok0 && v0 < v1) ok0 = 0;\n', 'r': 'if (v0 < v1 && ok0) ok0 = 0;\n', 'q': 'if (ok0) if (v0 < v1) ok0 = 0;\n', 'x': 'if (ok0 && v0 >= v1) { } else ok0 = 0;\n', 'n': 'if (v0 < v1) ok0 = 0;\n',
      'u': 'if (ok0 && v0 < v1) ok0 = 0;\n', 'k': 'ok0 = ok0 && v0 >= v1;\n'}
ST = {
    'm': f'if (!ok0 && ok1) {{ {S1} }}\n',
    'k': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'e': f'if (ok0 == 0 && ok1 != 0) {{ {S1} }}\n',
    'o': f'if (!(ok0 || !ok1)) {{ {S1} }}\n',
    'p': f'if (ok1 & !ok0) {{ {S1} }}\n',
    'b': f'if (!ok0 & (ok1 != 0)) {{ {S1} }}\n',
}
EN = {'r': f'if (!ok0) return 0;\n {S0}', 's': f'if (ok0) {{ {S0} }}\n return 0;\n'}
TAILS = {}
for ck, c in CL.items():
    for sk, s in ST.items():
        for ek, e in EN.items():
            TAILS[ck + sk + ek] = f'if (ok1) {{ {V1} {c} }} else {{ {I1} }}\n {s} {e}'
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
D = '	uint32_t v0, v1;\n	uint32_t ok0, ok1;\n'
TY = []
for a0, tv0 in (('u', 'uint32_t'), ('i', 'int')):
    for a1, tv1 in (('u', 'uint32_t'), ('i', 'int')):
        if tv0 == 'int' and tv1 == 'int':
            continue
        for a2, to0 in (('u', 'uint32_t'), ('i', 'int')):
            for a3, to1 in (('u', 'uint32_t'), ('i', 'int')):
                TY.append((a0 + a1 + a2 + a3, [(D, f'	{tv0} v0;\n	{tv1} v1;\n	{to0} ok0;\n	{to1} ok1;\n')]))
AXES = [AX, TY]
