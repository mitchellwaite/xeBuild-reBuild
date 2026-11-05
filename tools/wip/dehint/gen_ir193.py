"""findAnchor, no literal asm: the older block's flag cleared INSIDE ok1's valid arm, S1 tested there too, so S1's string expands before I1.
Types of ok0, ok1 and v0, v1 as a second axis (attempt 13)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irfa import *
FOCUS = ['_findAnchor']
CLR = {
    'a': 'if (ok0) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'b': 'if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; }\n',
    'c': 'if (ok0) { if (v0 >= v1) ok1 = 0; else ok0 = 0; }\n',
    'd': 'if (ok0 && v0 < v1) ok0 = 0;\n if (ok0) ok1 = 0;\n',
    'e': 'if (ok0) { if (v0 < v1) ok0 = 0; }\n if (ok0) ok1 = 0;\n',
    'f': 'if (ok0 && v0 >= v1) ok1 = 0;\n',
    'g': 'if (ok0) { if (v0 >= v1) ok1 = 0; }\n',
}
TAILS = {}
for k, c in CLR.items():
    TAILS['A' + k] = f'if (ok1) {{ {V1} {c} if (ok1) {{ {S1} }} }} else {{ {I1} }}\n {SEL0}'
    TAILS['B' + k] = f'if (!ok1) {{ {I1} }} else {{ {V1} {c} if (ok1) {{ {S1} }} }}\n {SEL0}'
    TAILS['C' + k] = f'if (ok1) {{ {V1} {c} if (ok1) {{ {S1} }} {S0} }}\n {I1} {SEL0}'
    TAILS['D' + k] = f'if (ok1) {{ {V1} {c} if (!ok1) goto s0; {S1} }}\n {I1} if (!ok0) return 0;\n s0: {S0}'
    TAILS['E' + k] = f'if (ok1) {{ {V1} {c} }} else {{ {I1} }}\n if (ok1) {{ {S1} }}\n {SEL0}'
AX = [(k, [(OLD, HEADV0 + v + '}\n')]) for k, v in TAILS.items()]
ASM = '''		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
'''
TY = [('uu', []),
      ('ii', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')]),
      ('ss', [('	uint32_t v0, v1;\n	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n	uint32_t v1, v0;\n')])]
AXES = [AX, TY]
