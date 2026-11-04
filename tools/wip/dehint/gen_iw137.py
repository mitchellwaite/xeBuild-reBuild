# attempt 8: imgAddFile's own forms (nothing depends on its names; it isn't inlined): its big copy's compare and the 0x30/0x34 slots.  IWB= base.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n6.c')
FOCUS = ['_imgAddFile']
AR = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
'''
B = '			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n'
S = '			imgAdd(off, data, len, 0, 0xffff, 1);\n'
ARF = [
 ('', []),
 ('a1', [(AR, '		if (xb.bigBlock)\n' + B + '		else\n' + S)]),
 ('a2', [(AR, '		if (xb.bigBlock > 0)\n' + B + '		else\n' + S)]),
 ('a3', [(AR, '		if (xb.bigBlock <= 0)\n' + S + '		else\n' + B)]),
 ('a4', [(AR, '		if (xb.bigBlock != 1)\n' + S + '		else\n' + B)]),
 ('a5', [(AR, '		if (xb.bigBlock == 1)\n' + B + '		else\n' + S)]),
]
H = '''		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
'''
HF = [
 ('', []),
 ('h1', [(H, '''		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)((off >> 14) - xb.fsStart));
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
''')]),
 ('h2', [(H, '''		uint16_t blk = (off >> 14) - xb.fsStart;

		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
''')]),
 ('h3', [(H, '''		int n = nFsFiles;

		fsFiles[n].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[n].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[n].name, name);
		fsFiles[n].time = *time;
''')]),
]
FT = '	if (imgFits(off, len)) {\n		fsFiles[nFsFiles]'
OFF = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n'
OF = [
 ('', []),
 ('o1', [(OFF, '	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n\n	if (imgFits(off, len)) {\n')]),
 ('o2', [(OFF, '	uint32_t off;\n\n	off = imgSizeAligned();\n	if (imgFits(off, len)) {\n')]),
 ('o3', [(OFF + '', '	uint32_t off = imgSizeAligned();\n\n	if (!imgFits(off, len)) {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n		return;\n	}\n	{\n'),
         ('	} else {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n	}\n', '	}\n')]),
]
AXES = [ARF, HF, OF]
