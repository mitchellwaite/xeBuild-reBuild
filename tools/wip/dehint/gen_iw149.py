# attempt 8: n6 family (clones right with `if (partial)`): spellings of the 73% test x t forms x pages place.  The test moves constprop.4's blocks + ivtmp.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n6.c')
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
C0 = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
T3 = 'len % 512 ? (len + 512) / 512 : len / 512'
NF = [
 ('a', '		if (partial > 0) {\n' + C + '		} else\n			npages = 32;\n'),
 ('d', '		npages = 32;\n		if (partial > 0) {\n' + C + '		}\n'),
 ('e', '		if (partial <= 0)\n			npages = 32;\n		else {\n' + C + '		}\n'),
 ('h', '		npages = partial > 0 ? (' + T3 + ') : 32;\n'),
 ('i', '		if (partial > 0)\n			npages = ' + T3 + ';\n		else\n			npages = 32;\n'),
 ('i2', '		if (partial <= 0)\n			npages = 32;\n		else\n			npages = ' + T3 + ';\n'),
 ('j', C0 + '		if (partial <= 0)\n			npages = 32;\n'),
 ('k', '		if (partial > 0) {\n			npages = len / 512;\n			if (len % 512)\n				npages++;\n		} else\n			npages = 32;\n'),
 ('l', '		if (partial > 0) {\n			if (len % 512)\n				npages = len / 512 + 1;\n			else\n				npages = len / 512;\n		} else\n			npages = 32;\n'),
 ('m', '		npages = 32;\n		if (partial > 0)\n			npages = ' + T3 + ';\n'),
]
TD = '	unsigned t;\n'
TC = 'if ((uint8_t)t < 15) {'
A = '			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;\n'
PIN = '			__asm__("" :: "g"(t));\n'
TF = [
 ('ui', []),
 ('uip', [(A, PIN + A)]),
 ('u8p', [(TD, '	uint8_t t;\n'), (TC, 'if (t < 15) {'), (A, PIN + A)]),
 ('chp', [(TD, '	char t;\n'), (A, PIN + A)]),
 ('inp', [(TD, '	int t;\n'), (A, PIN + A)]),
]
BIGPG = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct spb *)s)->b2lo'
SMPG = '					pages = len % 512 ? len / 512 + 1 : len / 512;\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n'
POS = [
 ('', []),
 ('Bi', [(BIGPG, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n				((struct spb *)s)->b2lo')]),
]
AXES = [[(a, [(N, b)]) for a, b in NF], TF, POS]
