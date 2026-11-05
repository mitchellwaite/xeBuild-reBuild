"""findAnchor, no literal asm (attempt 15): gen_ir212 `anr` with values on the older-block arm that dom2 can thread (constants in the join's PHIs), so V0's V1 reaches S0 with no test left."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
HEADS = {
    '1': ('use1 = ok1; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { use1 = 0; ok0 = 1; } }\n', 'ok0', 'use1', '!ok1'),
    '2': ('use1 = ok1; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { use1 = 0; ok1 = 1; } }\n', 'ok0', 'use1', '!ok1'),
    '3': ('use1 = ok1; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { use1 = 0; ok0 = 1; ok1 = 1; } }\n', 'ok0', 'use1', '!ok1'),
    '4': ('use0 = ok0; use1 = ok1; ', 'if (ok0 && ok1) { if (v0 < v1) use0 = 0; else { use0 = 1; use1 = 0; } }\n', 'use0', 'use1', '!ok1'),
    '5': ('use1 = ok1; inv = !ok1; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { use1 = 0; inv = 0; } }\n', 'ok0', 'use1', 'inv'),
    '6': ('use0 = ok0; use1 = ok1; inv = !ok1; ', 'if (ok0 && ok1) { if (v0 < v1) use0 = 0; else { use0 = 1; use1 = 0; inv = 0; } }\n', 'use0', 'use1', 'inv'),
    '7': ('use0 = ok0; use1 = ok1; inv = 0; ', 'if (!ok1) inv = 1; if (ok0 && ok1) { if (v0 < v1) use0 = 0; else { use0 = 1; use1 = 0; } }\n', 'use0', 'use1', 'inv'),
    '8': ('inv = !ok1; use0 = ok0; ', 'if (ok0 && ok1) { if (v0 < v1) use0 = 0; else { ok1 = 0; } }\n', 'use0', 'ok1', 'inv'),
    '9': ('inv = !ok1; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { ok1 = 0; } }\n', 'ok0', 'ok1', 'inv'),
    'a': ('inv = ok1 == 0; ', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { ok1 = 0; } }\n', 'ok0', 'ok1', 'inv'),
    'b': ('', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { ok1 = 2; } }\n', 'ok0', 'ok1 == 1', 'ok1 == 0'),
    'c': ('', 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else { ok1 = -1; } }\n', 'ok0', 'ok1 > 0', 'ok1 == 0'),
    'd': ('', 'if (ok0 && ok1) { if (v0 < v1) ok1 = 2; else { ok0 = 1; ok1 = 3; } }\n', 'ok0 && ok1 != 2', 'ok1', 'ok1 == 0'),
}
TAILS = {}
for hk, (pre, c, z, u, i) in HEADS.items():
    for sk, s in {'n': f'if (!({z})) {{ if ({u}) {{ {S1} }} }}\n', 'm': f'if (!({z}) && ({u})) {{ {S1} }}\n', 'p': f'if ({u}) {{ if (!({z})) {{ {S1} }} }}\n'}.items():
        for ek, e in {'r': f'if ({i}) {{ {I1} }}\n if (!({z})) return 0;\n {S0}', 's': f'if ({i}) {{ {I1} }}\n if ({z}) {{ {S0} }}\n return 0;\n'}.items():
            for vk, v in {'v': f'if (ok1) {V1}'}.items():
                TAILS[hk + sk + ek] = v + pre + c + s + e
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1, use0, use1;\n	int inv;\n')]),
      ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1, use0, use1, inv;\n')])]
AXES = [AX, TY]
