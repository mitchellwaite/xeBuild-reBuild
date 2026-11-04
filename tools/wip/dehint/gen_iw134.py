# attempt 8: from n4p (lnp2 gone, pin_t kept, pages in the arms): imgAddFile's 0x30/0x34 slots want npages' guard block hotter than 450.
# Predicted forms of the partial test x partial's forms, IWB= base.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n4p.c')
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
NF = [('n1', N),
 ('n2', '		if (partial <= 0)\n			npages = 32;\n		else {\n' + C + '		}\n'),
 ('n3', '		if (partial > 0) {\n' + C + '		} else\n			npages = 32;\n'),
 ('n3e', '		if (partial == 1) {\n' + C + '		} else\n			npages = 32;\n'),
 ('n3n', '		if (partial != 1)\n			npages = 32;\n		else {\n' + C + '		}\n'),
 ('n5', '		npages = 32;\n		if (partial > 0) {\n' + C + '		}\n'),
 ('n5e', '		npages = 32;\n		if (partial == 1) {\n' + C + '		}\n'),
 ('n6', '		npages = 32;\n		if (partial >= 1) {\n' + C + '		}\n'),
]
P = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
PF = [('p1', P),
 ('p3', "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"),
 ('p4', "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n"),
]
AXES = [[(a, [(N, b)]) for a, b in NF], [(a, [(P, b)]) for a, b in PF]]
