# attempt 12: P(big) 57..60 in imgAddFile puts the slots right (iw12probe `big`). 61% is the early-return hitrate. Forms that could carry an early return on the small arm: helpers holding the two calls, with or without a value.
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
FN = 'void imgAddFile(const char *name, const void *data, const uint32_t *time, uint32_t len)\n{\n	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n'
def helper(sig, body, call):
    return [(ARMS, '		' + call + '\n' + TAIL), (FN, sig + '\n{\n' + body + '}\n\n' + FN)]
A = [('', []),
 ('h1', helper('static void addFileData(uint32_t off, const void *data, uint32_t len)',
   '	if (!xb.bigBlock) {\n		imgAdd(off, data, len, 0, 0xffff, 1);\n		return;\n	}\n	imgAdd(off, data, len, 0x2a, 0xffff, 1);\n', 'addFileData(off, data, len);')),
 ('h2', helper('static int addFileData(uint32_t off, const void *data, uint32_t len)',
   '	if (!xb.bigBlock)\n		return imgAdd(off, data, len, 0, 0xffff, 1);\n	return imgAdd(off, data, len, 0x2a, 0xffff, 1);\n', 'addFileData(off, data, len);')),
 ('h3', helper('static void addFileData(uint32_t off, const void *data, uint32_t len)',
   '	if (xb.bigBlock) {\n		imgAdd(off, data, len, 0x2a, 0xffff, 1);\n		return;\n	}\n	imgAdd(off, data, len, 0, 0xffff, 1);\n', 'addFileData(off, data, len);')),
 ('h4', helper('static int addFileData(uint32_t off, const void *data, uint32_t len)',
   '	if (xb.bigBlock)\n		return imgAdd(off, data, len, 0x2a, 0xffff, 1);\n	return imgAdd(off, data, len, 0, 0xffff, 1);\n', 'addFileData(off, data, len);')),
 ('h5', helper('static void addFileData(uint32_t off, const void *data, uint32_t len)',
   '	if (!xb.bigBlock)\n		imgAdd(off, data, len, 0, 0xffff, 1);\n	else\n		imgAdd(off, data, len, 0x2a, 0xffff, 1);\n', 'addFileData(off, data, len);')),
 ('e1', [(ARMS, '''		if (!xb.bigBlock) {
			imgAdd(off, data, len, 0, 0xffff, 1);
			nFsFiles++;
			return;
		}
		imgAdd(off, data, len, 0x2a, 0xffff, 1);
''' + TAIL)]),
]
AXES = [A]
FLAGS = []
