# attempt 7: on a7 with lnp2 -> `partial <= 0`: only imgAddFile's slots 0x30/0x34 swap (r139 off+len vs r181 npages): forms local to imgAddFile
import os
N = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
BL = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
CALL = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
'''
HEADF = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n		fsFiles'
FITS = '	if ((xb.fsEnd - 1) * 0x4000 >= off + len)\n		return 1;\n	return 0;\n'
AXES = [
 [('le', [(N, '		if (partial <= 0)\n			npages = 32;\n')]),
  ('lz', [(N, '		if (partial <= 0)\n			npages = 32;\n		else\n			;\n')]),
 ],
 [('', []),
  ('b1', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((off >> 14) - xb.fsStart);\n')]),
  ('b2', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)((off >> 14) - xb.fsStart));\n')]),
 ],
 [('', []),
  ('c1', [(CALL, '		if (xb.bigBlock)\n			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n		else\n			imgAdd(off, data, len, 0, 0xffff, 1);\n')]),
  ('c2', [(CALL, '		imgAdd(off, data, len, xb.bigBlock ? 0x2a : 0, 0xffff, 1);\n')]),
  ('c3', [(CALL, '		imgAdd(off, data, len, !xb.bigBlock ? 0 : 0x2a, 0xffff, 1);\n')]),
 ],
 [('', []),
  ('e2', [(HEADF, '	uint32_t off = imgSizeAligned();\n	int ok = imgFits(off, len);\n\n	if (ok) {\n		fsFiles')]),
  ('e3', [(HEADF, '	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n\n	if (imgFits(off, len)) {\n		fsFiles')]),
 ],
 [('', []),
  ('f1', [(FITS, '	if (off + len <= (xb.fsEnd - 1) * 0x4000)\n		return 1;\n	return 0;\n')]),
  ('f2', [(FITS, '	if ((xb.fsEnd - 1) * 0x4000 < off + len)\n		return 0;\n	return 1;\n')]),
  ('f3', [(FITS, '	uint32_t end = off + len;\n\n	if ((xb.fsEnd - 1) * 0x4000 >= end)\n		return 1;\n	return 0;\n')]),
 ],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a7.c')
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_imgAddFileAs', '_imgAddMobile', '_addSmcConfig', '_writeInitialHeader', '_checkBootImage', '_finalizeImage', '_imgAddRaw']
