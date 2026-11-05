"""findAnchor, no literal asm (attempt 15): the families of gen_ir214 whose final chain is the reference's (`nr`), with predictor forms on the tests, since what's left is layout (P(ok1), P(v0 < v1)) and ok0/v1's registers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
HEADS = {
    '2': ('use1 = ok1; ', 'ok0', 'use1', '!ok1', lambda T, A: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; ok1 = 1; }} }}\n'),
    '3': ('use1 = ok1; ', 'ok0', 'use1', '!ok1', lambda T, A: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; ok0 = 1; ok1 = 1; }} }}\n'),
    '5': ('use1 = ok1; inv = !ok1; ', 'ok0', 'use1', 'inv', lambda T, A: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ use1 = 0; inv = 0; }} }}\n'),
    '6': ('use0 = ok0; use1 = ok1; inv = !ok1; ', 'use0', 'use1', 'inv', lambda T, A: f'if (ok0 && ok1) {{ {T} use0 = 0; else {{ use0 = 1; use1 = 0; inv = 0; }} }}\n'),
    '8': ('inv = !ok1; use0 = ok0; ', 'use0', 'ok1', 'inv', lambda T, A: f'if (ok0 && ok1) {{ {T} use0 = 0; else {{ ok1 = 0; }} }}\n'),
    '9': ('inv = !ok1; ', 'ok0', 'ok1', 'inv', lambda T, A: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ ok1 = 0; }} }}\n'),
    'c': ('', 'ok0', 'ok1 > 0', 'ok1 == 0', lambda T, A: f'if (ok0 && ok1) {{ {T} ok0 = 0; else {{ ok1 = -1; }} }}\n'),
}
VT = {'p': 'if (v0 < v1)', 'g': 'n = v0 < v1; if (n > 0)', 'l': 'n = v0 >= v1; if (n <= 0)'}
FT = {'p': f'if (ok1) {V1}', 'g': f'n1 = ok1 != 0; if (n1 > 0) {V1}', 'e': f'if (!ok1) {{ }} else {V1}'}
IT = {'p': lambda i: f'if ({i}) {{ {I1} }}\n', 'g': lambda i: f'm = {i}; if (m > 0) {{ {I1} }}\n'}
HV = {
    'p': HEADV0,
    'g': SHA0 + f'n0 = ok0 != 0; if (n0 > 0) {V0} else {{ {I0} }}\n' + SHA1,
    'l': SHA0 + f'n0 = ok0 != 0; if (n0 <= 0) {{ {I0} }} else {V0}\n' + SHA1,
}
TAILS = {}
for hk, (pre, z, u, i, c) in HEADS.items():
    for vk, v in VT.items():
        for fk, f in FT.items():
            for ik, it in IT.items():
                for hv, h in HV.items():
                    TAILS[hk + vk + fk + ik + hv] = h + f + pre + c(v, None) + f'if (!({z})) {{ if ({u}) {{ {S1} }} }}\n' + it(i) + f'if (!({z})) return 0;\n {S0}'
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1, use0, use1;\n	int inv, n, n0, n1, m;\n')])]
AXES = [AX, TY]
