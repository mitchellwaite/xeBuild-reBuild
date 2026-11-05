"""Pieces of findAnchor for generators (gen_ir94 on): OLD is src's text from the first sha call to the end."""
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
OLD_START = '	ok0 = shaSelfCheck(xb.dump + 0x2fe8000);\n'
OLD_END = '''		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
}
'''
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
HEADV0 = SHA0 + f'if (ok0) {V0} else {{ {I0} }}\n' + SHA1
RET0 = 'return 0;\n'
SEL0 = f'if (ok0) {{ {S0} }} ' + RET0
