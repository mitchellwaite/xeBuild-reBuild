# attempt 11: on build/iw/a11/g1.c.  imgAddFile's slots need head : guard about 317 : 450, while bbro needs the error arm's frequency >= head/2 (exec threshold of round 1), so P(fits) stays 50%.  So raise P(big arm), which also lowers the head relative to the loop:
# an early return on the small arm (PRED_TREE_EARLY_RETURN, 39%).
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g1.c')
CALL = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		nFsFiles++;
'''
S = '			imgAdd(off, data, len, 0, 0xffff, 1);\n'
B = '			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n'
AXES = [[
 ('', []),
 ('b', [(CALL, '		if (!xb.bigBlock) {\n' + S + '			nFsFiles++;\n			return;\n		}\n' + B[1:] + '		nFsFiles++;\n')]),
 ('c', [(CALL, '		if (!xb.bigBlock) {\n' + S + '			nFsFiles++;\n			return;\n		} else {\n' + B + '			nFsFiles++;\n		}\n')]),
 ('d', [(CALL, '		if (!xb.bigBlock) {\n' + S + '			nFsFiles++;\n		} else {\n' + B + '			nFsFiles++;\n		}\n')]),
 ('e', [(CALL, '		if (xb.bigBlock) {\n' + B + '			nFsFiles++;\n			return;\n		}\n' + S[1:] + '		nFsFiles++;\n')]),
 ('f', [(CALL, '		if (xb.bigBlock)\n' + B + '		else {\n' + S + '			nFsFiles++;\n			return;\n		}\n		nFsFiles++;\n')]),
 ('g', [(CALL, '		if (!xb.bigBlock) {\n' + S + '		} else {\n' + B + '			nFsFiles++;\n			return;\n		}\n		nFsFiles++;\n')]),
]]
FLAGS = []
