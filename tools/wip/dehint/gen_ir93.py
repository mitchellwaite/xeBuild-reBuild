"""findAnchor with no hint at all: whole-function shapes, including `Linux` readings (sel1 before sel0, flags cleared).
tmp/xeBuild64's findAnchor: ok0; v/i; ok1: valid, ok0==0 -> S1, v0>=v1 -> S0, S1.  invalid, ok0 -> S0, return 0."""
FOCUS = ['_findAnchor']
OLD_START = '	ok0 = shaSelfCheck(xb.dump + 0x2fe8000);\n'
OLD_END = '''		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
}
'''
import re, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
a = src.index(OLD_START)
b = src.index(OLD_END, a) + len(OLD_END)
OLD = src[a:b]
S0C = 'log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);\n memcpy(anchor, xb.dump + 0x2fe8000, 0x200);\n'
S1C = 'log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);\n memcpy(anchor, xb.dump + 0x2fec000, 0x200);\n'
S0 = S0C + 'return 1;\n'
S1 = S1C + 'return 1;\n'
V0 = 'log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);\n'
I0 = 'log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");\n'
V1 = 'log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);\n'
I1 = 'log_printf(1, "anchor block at 0x2fec000 is invalid\\n");\n'
SHA0 = 'ok0 = shaSelfCheck(xb.dump + 0x2fe8000);\n'
SHA1 = 'ok1 = shaSelfCheck(xb.dump + 0x2fec000);\n'
HEAD = SHA0 + f'if (ok0) {V0} else {{ {I0} }}\n' + SHA1 + f'if (ok1) {V1} else {{ {I1} }}\n'
HEADN = SHA0 + f'if (!ok0) {{ {I0} }} else {V0}\n' + SHA1 + f'if (!ok1) {{ {I1} }} else {V1}\n'
TAILS = {
    'plain': f'if (ok0 && (!ok1 || v0 >= v1)) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'rev': f'if (ok1 && (!ok0 || v0 < v1)) {{ {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'nest': f'if (ok0) {{ if (ok1 && v0 < v1) {{ {S1} }} {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'nest2': f'if (ok1) {{ if (ok0 && v0 >= v1) {{ {S0} }} {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'nest3': f'if (ok1) {{ if (ok0) {{ if (v0 >= v1) {{ {S0} }} }} {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'nest4': f'if (ok0) {{ if (ok1) {{ if (v0 < v1) {{ {S1} }} }} {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'clr': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; else ok1 = 0; }} if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'clr1': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; else ok1 = 0; }} if (ok1) {{ {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'clr2': f'if (ok0 && ok1 && v0 < v1) ok0 = 0; if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'clr3': f'if (ok0 && ok1 && v0 >= v1) ok1 = 0; if (ok1) {{ {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'clr4': f'if (ok0 && ok1) {{ if (v0 >= v1) ok1 = 0; }} if (ok1) {{ {S1} }} if (ok0) {{ {S0} }} return 0;\n',
    'clr5': f'if (ok0 && ok1) {{ if (v0 < v1) ok0 = 0; }} if (ok0) {{ {S0} }} if (ok1) {{ {S1} }} return 0;\n',
    'sel': f'sel = -1; if (ok0) sel = 0; if (ok1) {{ if (sel < 0 || v0 < v1) sel = 1; }} if (sel == 0) {{ {S0} }} if (sel == 1) {{ {S1} }} return 0;\n',
    'ret': f'ret = 0; if (ok0 && (!ok1 || v0 >= v1)) {{ {S0C} ret = 1; }} else if (ok1) {{ {S1C} ret = 1; }} return ret;\n',
    'ret2': f'ret = 0; if (ok1 && (!ok0 || v0 < v1)) {{ {S1C} ret = 1; }} else if (ok0) {{ {S0C} ret = 1; }} return ret;\n',
    'ret3': f'ret = 0; if (ok0) {{ if (ok1 && v0 < v1) {{ {S1C} }} else {{ {S0C} }} ret = 1; }} else if (ok1) {{ {S1C} ret = 1; }} return ret;\n',
    'ret4': f'ret = 0; if (ok1) {{ if (ok0 && v0 >= v1) {{ {S0C} }} else {{ {S1C} }} ret = 1; }} else if (ok0) {{ {S0C} ret = 1; }} return ret;\n',
    'or': f'if (!ok0 && !ok1) return 0; if (ok1 && (!ok0 || v0 < v1)) {{ {S1} }} {S0}',
    'or1': f'if (!ok0 && !ok1) return 0; if (ok0 && (!ok1 || v0 >= v1)) {{ {S0} }} {S1}',
    'or2': f'if (ok0 || ok1) {{ if (ok1 && (!ok0 || v0 < v1)) {{ {S1} }} {S0} }} return 0;\n',
    'or3': f'if (ok0 || ok1) {{ if (ok0 && (!ok1 || v0 >= v1)) {{ {S0} }} {S1} }} return 0;\n',
}
AX = [(k + 'h', [(OLD, HEAD + v + '}\n')]) for k, v in TAILS.items()] + [(k + 'n', [(OLD, HEADN + v + '}\n')]) for k, v in TAILS.items()]
DECL = '	uint32_t ok0, ok1;\n'
AXES = [AX, [('', [(DECL, DECL + '	int sel, ret;\n')]), ('si', [(DECL, '	int ok0, ok1, sel, ret;\n')])]]
