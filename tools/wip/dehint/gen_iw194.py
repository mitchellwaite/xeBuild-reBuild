# attempt 12: net -1 route: P(big) must land in 57..60. A null test on a pointer already dereferenced is dead at VRP but gets PRED_TREE_POINTER (85%) at profile_estimate: P(big) = 1 - .5 * .85 = .575.
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
def small_big(c):
    return [(ARMS, '		if (' + c + ')\n			imgAdd(off, data, len, 0, 0xffff, 1);\n		else\n			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n' + TAIL)]
def big_small(c):
    return [(ARMS, '		if (' + c + ')\n			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n		else\n			imgAdd(off, data, len, 0, 0xffff, 1);\n' + TAIL)]
A = [('', []),
 ('D1', small_big('!xb.bigBlock && time')),
 ('D2', small_big('!xb.bigBlock && name')),
 ('D3', small_big('time && !xb.bigBlock')),
 ('D4', small_big('name && !xb.bigBlock')),
 ('D5', big_small('xb.bigBlock || !time')),
 ('D6', big_small('xb.bigBlock || !name')),
 ('D7', big_small('!time || xb.bigBlock')),
 ('D8', big_small('!name || xb.bigBlock')),
 ('D9', small_big('!xb.bigBlock && time != NULL')),
]
A += [('E1', big_small('xb.bigBlock && time')),
 ('E2', big_small('xb.bigBlock && name')),
 ('E3', small_big('!xb.bigBlock || !time')),
 ('E4', small_big('!xb.bigBlock || !name')),
 ('E5', big_small('xb.bigBlock && time != NULL')),
]
AXES = [A]
FLAGS = []
