# attempt 8: lnp2 and pin_t gone: npages forms x partial forms x t forms, from build/iw/a8/n2.c (n1p1 without the pin, `unsigned t`).
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n2.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
N = '''		if (partial) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
C = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
C0 = C.replace('\t\t\t', '\t\t').replace('\t\t\t\t', '\t\t\t')
C0 = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
NF = [
 ('n1', N),
 ('n2', '		if (partial <= 0)\n			npages = 32;\n		else {\n' + C + '		}\n'),
 ('n3', '		if (partial > 0) {\n' + C + '		} else\n			npages = 32;\n'),
 ('n4', '		npages = 32;\n		if (partial) {\n' + C + '		}\n'),
 ('n5', '		npages = 32;\n		if (partial > 0) {\n' + C + '		}\n'),
 ('n6', C0 + '		if (!partial)\n			npages = 32;\n'),
 ('n7', C0 + '		if (partial <= 0)\n			npages = 32;\n'),
 ('n8', '		npages = partial ? (len % 512 ? (len + 512) / 512 : len / 512) : 32;\n'),
 ('n9', '		if (!partial)\n			npages = 32;\n		else if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n'),
]
P = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
PF = [
 ('p1', P),
 ('p2', "		partial = type != 0 && type != '0' && len < 0x4000;\n"),
 ('p3', "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"),
 ('p4', "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n"),
]
TD = '	unsigned t;\n'
TC = 'if ((uint8_t)t < 15) {'
TF = [
 ('ti', []),
 ('tb', [(TD, '	uint8_t t;\n'), (TC, 'if (t < 15) {')]),
]
AXES = [
 [(a, [(N, b)]) for a, b in NF],
 [(a, [(P, b)]) for a, b in PF],
 TF,
]
