"""findAnchor, no literal asm (attempt 15): V1 and I1 as the two arms of one test (P(ok1) 50 from the calls), S1 tested inside the valid arm on ok0's flag after a both-valid selection; chain V1, S1, I1, S0."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
CL = {
    'a': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; }\n',
    'b': 'if (ok0 && v0 < v1) ok0 = 0;\n',
    'c': 'if (ok0) { if (v0 < v1) ok0 = 0; }\n',
    'd': 'if (v0 < v1) ok0 = 0;\n',
    'e': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 2; }\n',
    'f': 'if (ok0) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'g': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'h': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok0 = 1; }\n',
    'i': 'if (ok0) { if (v0 < v1) ok0 = 0; else ok0 = 1; }\n',
}
ST = {
    'n': f'if (!ok0) {{ {S1} }}\n',
    'o': f'if (!ok0) {{ if (ok1) {{ {S1} }} }}\n',
    'm': f'if (!ok0 && ok1) {{ {S1} }}\n',
    'k': f'if (ok1 && !ok0) {{ {S1} }}\n',
    'u': f'if (ok1 == 1) {{ if (!ok0) {{ {S1} }} }}\n',
    'e': f'if (ok0) goto sel0;\n {S1}',
    'f': f'if (ok0) {{ {S0} }}\n {S1}',
}
EN = {
    'r': f'if (!ok0) return 0;\n sel0:\n {S0}',
    's': f'if (ok0) {{ sel0:\n {S0} }}\n return 0;\n',
}
FORM = {
    'A': lambda c, s, e: f'if (ok1) {{ {V1} {c} {s} }} else {{ {I1} }}\n {e}',
    'B': lambda c, s, e: f'if (!ok1) {{ {I1} }} else {{ {V1} {c} {s} }}\n {e}',
    'C': lambda c, s, e: f'if (ok1) {{ {V1} {c} {s} goto sel0;\n }}\n {I1} {e}',
    'D': lambda c, s, e: f'if (ok1) {{ {V1} {c} }} else {{ {I1} }}\n {s} {e}',
    'E': lambda c, s, e: f'if (ok1) {{ {V1} {c} {s} if (ok1 < 0) {{ {I1} }} }} else {{ {I1} }}\n {e}',
}
del FORM['E']
TAILS = {}
for fk, f in FORM.items():
    for ck, c in CL.items():
        for sk, s in ST.items():
            for ek, e in EN.items():
                if fk == 'C' and sk in ('f',):
                    continue
                if sk == 'f' and 'sel0' not in e:
                    continue
                TAILS[fk + ck + sk + ek] = f(c, s, e)
DRAFT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt14.c'), newline='').read().replace('\r\n', '\n')
a = DRAFT.index(OLD_START)
b = DRAFT.index(OLD_END, a) + len(OLD_END)
OLDD = DRAFT[a:b]
AX = [(k, [(OLDD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
TY = [('uu', []), ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')])]
AXES = [AX, TY]
