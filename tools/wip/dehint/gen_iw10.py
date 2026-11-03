# imgAddFile: natural heads with none of its own tricks (end pin, dead tests, cold label, expect)
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddFile']
s = open(__file__.replace('gen_iw10.py', 'drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('void imgAddFile(const char *name')
b = s.index('void imgAddFileAs(const char *name')
OLD = s[a:b]
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
ERR = '''		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
'''
SIG = 'void imgAddFile(const char *name, const void *data, const uint32_t *time, uint32_t len)\n{\n'
HEADS = {
    'fits': ('	uint32_t off = imgSizeAligned();\n', 'imgFits(off, len)'),
    'lim': ('	uint32_t off = imgSizeAligned();\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n', 'lim >= off + len'),
    'end': ('	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n', 'imgFits(off, len)'),
    'lim-end': ('	uint32_t off = imgSizeAligned();\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n', 'lim >= end'),
    'end-lim': ('	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n', 'lim >= end'),
    'end-lim2': ('	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n', 'end <= lim'),
    'endin': ('	uint32_t off = imgSizeAligned();\n	uint32_t end = off + len;\n', '(xb.fsEnd - 1) * 0x4000 >= end'),
    'offin': ('	uint32_t off;\n	off = imgSizeAligned();\n', '(xb.fsEnd - 1) * 0x4000 >= off + len'),
}
ARMS = {
    'then': lambda c: f'	if ({c}) {{\n{BODY}	}} else {{\n{ERR}	}}\n}}\n\n',
    'ret': lambda c: f'	if (!({c})) {{\n{ERR}		return;\n	}}\n{BODY}}}\n\n',
    'else': lambda c: f'	if (!({c})) {{\n{ERR}	}} else {{\n{BODY}	}}\n}}\n\n',
    'early': lambda c: f'	if ({c}) {{\n{BODY}		return;\n	}}\n{ERR}}}\n\n',
}
AXES = [[(h + '+' + r, [(OLD, SIG + HEADS[h][0] + '\n' + ARMS[r](HEADS[h][1]))]) for h in HEADS for r in ARMS]]
