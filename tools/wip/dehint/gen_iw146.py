# attempt 8: n6 (lnp2, pin_t gone): imgAddFile's arm order: if the fits arm's probability rises (early return, PRED_CALL on the error arm only), npages' guard gets hotter than off+len.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n6.c')
FOCUS = ['_imgAddFile']
HEAD = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n'
BODY = '''		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		nFsFiles++;
'''
ERR = '		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n'
FULL = HEAD + BODY + '	} else {\n' + ERR + '	}\n'
D = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
OFF = '	uint32_t off = imgSizeAligned();\n\n'
FORMS = [
 ('', []),
 ('dead', [(FULL, OFF + D + FULL[len(OFF):])]),
 ('r1', [(FULL, OFF + '	if (!imgFits(off, len)) {\n' + ERR + '		return;\n	}\n' + BODY.replace('\t\t', '\t', 1))]),
 ('r2', [(FULL, HEAD + BODY + '		return;\n	}\n' + ERR.replace('\t\t', '\t', 1))]),
 ('r1d', [(FULL, OFF + D + '	if (!imgFits(off, len)) {\n' + ERR + '		return;\n	}\n' + BODY.replace('\t\t', '\t', 1))]),
 ('r2d', [(FULL, OFF + D + HEAD[len(OFF):] + BODY + '		return;\n	}\n' + ERR.replace('\t\t', '\t', 1))]),
 ('r3', [(FULL, OFF + '	if (imgFits(off, len) == 0) {\n' + ERR + '	} else {\n' + BODY + '	}\n')]),
 ('r3d', [(FULL, OFF + D + '	if (imgFits(off, len) == 0) {\n' + ERR + '	} else {\n' + BODY + '	}\n')]),
]
AXES = [FORMS]
