# attempt 8: n9 (`char t`, constprop.1 right): constprop.4's `blocks + ivtmp` wants blocks' version above ivtmp's.  Forms of the head's blocks x tail.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n9.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
H = '''		rem = len - first;
		tail = rem;
		if (rem >= 0x4000)
			tail = rem % 0x4000;
		blocks = rem / 0x4000;
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
'''
T0 = '''		tail = rem;
		if (rem >= 0x4000)
			tail = rem % 0x4000;
'''
TF = {'a': T0, 'b': '		tail = rem % 0x4000;\n', 'c': '		tail = rem < 0x4000 ? rem : rem % 0x4000;\n', 'd': '		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n		else\n			tail = rem;\n'}
BF = {
 'a': '		blocks = rem / 0x4000;\n		if (tail) {\n			blocks++;\n		}\n		if (x) {\n			blocks++;\n		}\n',
 'b': '		blocks = rem / 0x4000;\n		if (x) {\n			blocks++;\n		}\n		if (tail) {\n			blocks++;\n		}\n',
 'c': '		blocks = rem / 0x4000 + (tail != 0) + (x != 0);\n',
 'd': '		blocks = rem / 0x4000;\n		blocks += tail != 0;\n		blocks += x != 0;\n',
 'e': '		blocks = rem / 0x4000;\n		if (tail)\n			blocks++;\n		blocks += x != 0;\n',
 'f': '		blocks = rem / 0x4000;\n		blocks += tail != 0;\n		if (x)\n			blocks++;\n',
 'g': '		blocks = (tail ? rem / 0x4000 + 1 : rem / 0x4000);\n		if (x)\n			blocks++;\n',
 'h': '		if (tail)\n			blocks = rem / 0x4000 + 1;\n		else\n			blocks = rem / 0x4000;\n		if (x)\n			blocks++;\n',
 'i': '		blocks = rem / 0x4000 + (tail ? 1 : 0);\n		if (x)\n			blocks++;\n',
 'j': '		blocks = (rem + 0x3fff) / 0x4000;\n		if (x)\n			blocks++;\n',
}
AX = []
for t, tv in TF.items():
    for b, bv in BF.items():
        AX.append(('T%s+B%s' % (t, b), [(H, '		rem = len - first;\n' + tv + bv)]))
AXES = [AX]
