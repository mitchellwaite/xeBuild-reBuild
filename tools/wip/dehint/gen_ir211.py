"""findAnchor, no literal asm (attempt 15): S1 textually before I1 by way of separate selection state, so `ok1` still tells I1's test
what the sha said: use0/use1 copies, or one `sel` variable.  Base: the draft with the asm in; the asm goes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
SEL = {
    'c1': 'use0 = ok0; use1 = ok1; if (ok0 && ok1) { if (v0 < v1) use0 = 0; else use1 = 0; }\n',
    'c2': 'use0 = ok0; use1 = ok1; if (use0 && use1) { if (v0 < v1) use0 = 0; else use1 = 0; }\n',
    'c3': 'use0 = ok0; use1 = ok1; if (ok0 && ok1 && v0 < v1) use0 = 0; if (use0) use1 = 0;\n',
    'c4': 'use1 = ok1; use0 = ok0; if (ok0) { if (ok1) { if (v0 < v1) use0 = 0; else use1 = 0; } }\n',
    'c5': 'use1 = ok1 && (!ok0 || v0 < v1); use0 = !use1 && ok0;\n',
    'c6': 'use1 = ok1; if (ok0 && ok1 && v0 >= v1) use1 = 0; use0 = ok0 && !use1;\n',
    'c7': 'use1 = 0; use0 = 0; if (ok1) { if (!ok0 || v0 < v1) use1 = 1; else use0 = 1; } else if (ok0) use0 = 1;\n',
    'c8': 'use0 = ok0; use1 = 0; if (ok1) { if (!ok0 || v0 < v1) { use0 = 0; use1 = 1; } }\n',
    'c9': 'use0 = ok0; use1 = ok1; if (ok1) { if (ok0) { if (v0 < v1) use0 = 0; else use1 = 0; } }\n',
}
T1 = {'a': f'if (use1) {{ {S1} }}\n', 'b': f'if (use1 > 0) {{ {S1} }}\n'}
TI = {'n': f'if (!ok1) {{ {I1} }}\n', 'p': f'if (ok1 == 0) {{ {I1} }}\n'}
T0 = {'s': f'if (use0) {{ {S0} }}\n return 0;\n', 'r': f'if (!use0) return 0;\n {S0}'}
HV = {'v': f'if (ok1) {V1}'}
SELV = {  # one variable
    'd1': f'sel = -1; if (ok0) sel = 0; if (ok1) {{ if (sel < 0 || v0 < v1) sel = 1; }}\n if (sel == 1) {{ {S1} }}\n if (!ok1) {{ {I1} }}\n if (sel == 0) {{ {S0} }}\n return 0;\n',
    'd2': f'sel = ok0 ? 0 : -1; if (ok1 && (sel < 0 || v0 < v1)) sel = 1;\n if (sel == 1) {{ {S1} }}\n if (!ok1) {{ {I1} }}\n if (sel < 0) return 0;\n {S0}',
    'd3': f'sel = 0; if (ok0) sel = 1; if (ok1) {{ if (!ok0 || v0 < v1) sel = 2; }}\n if (sel == 2) {{ {S1} }}\n if (!ok1) {{ {I1} }}\n if (sel) {{ {S0} }}\n return 0;\n',
    'd4': f'sel = 0; if (ok1) sel = 2; if (ok0) {{ if (!ok1 || v0 >= v1) sel = 1; }}\n if (sel == 2) {{ {S1} }}\n if (!ok1) {{ {I1} }}\n if (sel) {{ {S0} }}\n return 0;\n',
    'd5': f'sel = 0; if (ok1) sel = 2; if (ok0) {{ if (!ok1 || v0 >= v1) sel = 1; }}\n switch (sel) {{ case 2: {S1} }}\n if (!ok1) {{ {I1} }}\n if (sel) {{ {S0} }}\n return 0;\n',
}
TAILS = {}
for s, cs in SEL.items():
    for a, c1 in T1.items():
        for n, ci in TI.items():
            for z, c0 in T0.items():
                TAILS[s + a + n + z] = HV['v'] + cs + c1 + ci + c0
for k, v in SELV.items():
    TAILS[k] = HV['v'] + v
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1;\n	int use0, use1, sel;\n')]),
      ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n	int use0, use1, sel;\n')]),
      ('nn', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0, ok1, use0, use1;\n	int sel;\n')])]
AXES = [AX, TY]
