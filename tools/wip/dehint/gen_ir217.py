"""findAnchor, no literal asm (attempt 15): gen_ir216 with ok1 as an int truth value everywhere: `int ok1 = sha != 0; if (ok1 > 0)`, so positive 73 cancels V1's call with no second variable between J and the tests."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
HEADS = {
    '2': ('use1 = ok1; ', 'ok0', 'use1', '!ok1', lambda T: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; ok1 = 1; }} }}\n'),
    '3': ('use1 = ok1; ', 'ok0', 'use1', '!ok1', lambda T: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; ok0 = 1; ok1 = 1; }} }}\n'),
    '5': ('use1 = ok1; inv = !ok1; ', 'ok0', 'use1', 'inv', lambda T: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; inv = 0; }} }}\n'),
    '8': ('inv = !ok1; use0 = ok0; ', 'use0', 'ok1', 'inv', lambda T: f'if (ok0 && ok1) {{ {T} use0 = 0; else {{ ok1 = 0; }} }}\n'),
    '9': ('inv = !ok1; ', 'ok0', 'ok1', 'inv', lambda T: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ ok1 = 0; }} }}\n'),
    'd': ('use1 = ok1; ', 'ok0', 'use1', '!ok1', lambda T: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; }} }}\n'),
}
SHAS = {'n': 'ok1 = shaSelfCheck(xb.dump + 0x2fec000) != 0;\n', 'b': 'ok1 = !!shaSelfCheck(xb.dump + 0x2fec000);\n', 'r': 'ok1 = shaSelfCheck(xb.dump + 0x2fec000) ? 1 : 0;\n'}
VT = {'p': 'if (v0 < v1)', 'g': 'n = v0 < v1; if (n > 0)'}
FT = {'g': f'if (ok1 > 0) {V1}', 'p': f'if (ok1) {V1}', 'l': f'if (ok1 <= 0) {{ }} else {V1}'}
IT = {'p': lambda i: f'if ({i}) {{ {I1} }}\n', 'l': lambda i: f'if (ok1 <= 0) {{ {I1} }}\n'}
HV = {'p': SHA0 + f'if (ok0) {V0} else {{ {I0} }}\n'}
TAILS = {}
for hk, (pre, z, u, i, c) in HEADS.items():
    for sk, sh in SHAS.items():
        for vk, v in VT.items():
            for fk, f in FT.items():
                for ik, it in IT.items():
                    if ik == 'l' and hk not in ('2', '3', 'd'):
                        continue
                    TAILS[hk + sk + vk + fk + ik] = HV['p'] + sh + f + pre + c(v) + f'if (!({z})) {{ if ({u}) {{ {S1} }} }}\n' + it(i) + f'if (!({z})) return 0;\n {S0}'
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, use0; int ok1, use1, inv, n;\n')])]
AXES = [AX, TY]
