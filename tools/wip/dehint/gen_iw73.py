# attempt 5: partial's type and form x t's position x npages x c4 x lnp2, on m1 (natural imgFits, imgAddFile, imgAddMobile)
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
DECL = '	int partial;\n'
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
T = "		t = type - '1';\n"
LAB = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
AXES = [
 [(k, [(DECL, '	%s partial;\n' % k)] if k != 'int' else []) for k in ('int', 'uint8_t', 'char', 'signed char', 'short', 'uint16_t', 'uint32_t', 'long', '_Bool')],
 [('', []),
  ('pa', [(P, "		partial = 0;\n		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n")]),
  ('pb', [(P, "		partial = 1;\n		if (type == 0 || type == '0' || len >= 0x4000)\n			partial = 0;\n")]),
  ('pc', [(P, "		partial = (type != 0) && (type != '0') && (len < 0x4000) ? 1 : 0;\n")]),
  ('pd', [(P, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
 ],
 [('', []), ('tb', [(P + T, T + P)])],
 [('', []), ('l2', [(LAB, '		if (!partial)\n			npages = 32;\n')])],
 [('', []), ('c4', [(C4, '')])],
]
FLAGS = []
