"""findAnchor, no literal asm (attempt 15): grammar of tails with the text in .rdata's order V1, S1, I1, S0.  z says use block 0, u says block 1; both-valid clears z when 1 is newer."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
PRES = {'p0': ('', 'ok0', 'ok1'), 'p1': ('use1 = ok1;\n', 'ok0', 'use1'), 'p2': ('use0 = ok0;\n', 'use0', 'ok1'), 'p3': ('use0 = ok0;\n use1 = ok1;\n', 'use0', 'use1')}
OUT = {  # after `if (ok1) V1`
    'c1': 'if (ok0 && ok1) { if (v0 < v1) Z = 0; }\n',
    'c2': 'if (ok0 && ok1 && v0 < v1) Z = 0;\n',
    'c3': 'if (ok0) { if (ok1) { if (v0 < v1) Z = 0; } }\n',
    'c4': 'if (ok1) { if (ok0) { if (v0 < v1) Z = 0; } }\n',
    'c5': 'if (ok1) { if (ok0 && v0 < v1) Z = 0; }\n',
    'c6': 'if (ok0) { if (ok1 && v0 < v1) Z = 0; }\n',
    'c7': 'if (ok1 && v0 < v1) Z = 0;\n',
    'c8': 'if (ok1) { if (v0 < v1) Z = 0; }\n',
    'c9': 'if (ok0 && ok1) { if (v0 < v1) Z = 0; else U = 0; }\n',
    'ca': 'if (ok0) { if (ok1) { if (v0 < v1) Z = 0; else U = 0; } }\n',
}
INSIDE = {  # inside the V1 arm
    'i1': 'if (ok0) { if (v0 < v1) Z = 0; }\n',
    'i2': 'if (ok0 && v0 < v1) Z = 0;\n',
    'i3': 'if (v0 < v1) Z = 0;\n',
    'i4': 'if (ok0) { if (v0 < v1) Z = 0; else U = 0; }\n',
}
SS = {'n': 'if (!Z) { if (U) { SONE } }\n', 'm': 'if (!Z && U) { SONE }\n', 'p': 'if (U) { if (!Z) { SONE } }\n'}
EE = {'r': 'if (!ok1) { IONE }\n if (!Z) return 0;\n SNIL', 's': 'if (!ok1) { IONE }\n if (Z) { SNIL }\n return 0;\n'}
TAILS = {}
for pk, (pre, z, u) in PRES.items():
    for sk, s in SS.items():
        for ek, e in EE.items():
            for ck, c in OUT.items():
                if 'U = 0' in c and u == 'ok1':
                    continue
                TAILS[pk + ck + sk + ek] = f'if (ok1) {V1}' + pre + c + s + e, z, u
            for ck, c in INSIDE.items():
                if 'U = 0' in c and u == 'ok1':
                    continue
                TAILS[pk + ck + sk + ek] = pre + f'if (ok1) {{ {V1}' + c + '}\n' + s + e, z, u


def fill(t, z, u):
    return t.replace('Z', z).replace('U', u).replace('SONE', S1).replace('IONE', I1).replace('SNIL', S0)


DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + fill(t, z, u) + '}\n')]) for k, (t, z, u) in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1, use0, use1;\n')]),
      ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1, use0, use1;\n')])]
AXES = [AX, TY]
