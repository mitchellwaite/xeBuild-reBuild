# attempt 12: net -1 route, broad: one dead test local to imgAddFile, hunting P(big) in 57..60 (head 322..339): dead conditions (predictors 85, 72, 73 and none) x shapes around the two calls. Looks only at imgAddFile's lines.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near11.c')
ARMS = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		nFsFiles++;
	} else {
		log_printf(0, "\\n******* ERROR: adding %s will exceed'''
TAIL = '''		nFsFiles++;
	} else {
		log_printf(0, "\\n******* ERROR: adding %s will exceed'''
S = '			imgAdd(off, data, len, 0, 0xffff, 1);\n'
B = '			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n'
XS = {'tm': 'time', 'ntm': '!time', 'ne': '(off & 0x3fff) != 0x4000', 'eq': '(off & 0x3fff) == 0x4000', 'gt': '(off & 0x3fff) > 0x3fff', 'le': '(off & 0x3fff) <= 0x3fff', 'po': '(int)(off & 0x3fff) > -1', 'ng': '(int)(off & 0x3fff) < 0'}
def ifs(c, a, b):
    return '		if (' + c + ')\n' + a + '		else\n' + b
SHAPES = {
 'A': lambda x: ifs('!xb.bigBlock && ' + x, S, B),
 'B': lambda x: ifs(x + ' && !xb.bigBlock', S, B),
 'C': lambda x: ifs('xb.bigBlock && ' + x, B, S),
 'D': lambda x: ifs(x + ' && xb.bigBlock', B, S),
 'E': lambda x: ifs('!xb.bigBlock || ' + x, S, B),
 'F': lambda x: ifs(x + ' || !xb.bigBlock', S, B),
 'G': lambda x: ifs('xb.bigBlock || ' + x, B, S),
 'H': lambda x: ifs(x + ' || xb.bigBlock', B, S),
 # a dead return ahead of one call
 'I': lambda x: '		if (!xb.bigBlock) {\n			if (' + x + ')\n				return;\n' + S + '		} else\n' + B,
 'J': lambda x: '		if (!xb.bigBlock)\n' + S + '		else {\n			if (' + x + ')\n				return;\n' + B + '		}\n',
 # a dead return ahead of the test
 'K': lambda x: '		if (' + x + ')\n			return;\n' + ifs('!xb.bigBlock', S, B),
 # dead arm with a call
 'L': lambda x: '		if (!xb.bigBlock) {\n			if (' + x + ')\n				log_printf(0, "%s", name);\n' + S + '		} else\n' + B,
 'M': lambda x: '		if (!xb.bigBlock)\n' + S + '		else {\n			if (' + x + ')\n				log_printf(0, "%s", name);\n' + B + '		}\n',
}
A = [('', [])]
for sn, sf in SHAPES.items():
    for xn, x in XS.items():
        A.append((sn + xn, [(ARMS, sf(x) + TAIL)]))
AXES = [A]
FLAGS = []
FOCUS = ['_imgAddFile']
