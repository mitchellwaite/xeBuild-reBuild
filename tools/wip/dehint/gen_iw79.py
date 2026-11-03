# attempt 5: on the 9-trick draft: partial's type and form x label x pin_t x opt x len++ x c4
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a5.c')
DECL = '	int partial;\n'
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
LAB = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
TESTS = "type != 0 && type != '0' && len < 0x4000"
PIN = '			__asm__("" :: "g"(t));\n'
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
L = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n	if (imgFits'
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
AXES = [
 [(k, [(DECL, '	%s partial;\n' % k)] if k != 'int' else []) for k in ('int', '_Bool', 'uint8_t')],
 [('p0', []),
  ('pa', [(P, "		partial = 0;\n		if (%s)\n			partial = 1;\n" % TESTS)]),
  ('and1', [(P, "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n")]),
 ],
 [('lab', []), ('le', [(LAB, '		if (partial <= 0)\n			npages = 32;\n')]), ('nolab', [(LAB, '		if (!partial)\n			npages = 32;\n')])],
 [('', []), ('nopin', [(PIN, '')])],
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
 [('', []), ('nol', [(L, '	if (imgFits')])],
 [('', []), ('noc4', [(C4, '')])],
]
FLAGS = []
