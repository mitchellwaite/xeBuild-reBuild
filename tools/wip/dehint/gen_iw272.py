# attempt 20: imgAddFile's own source forms on a P 50 base (its names are local; imgAdd's other functions don't depend on them). Base from IWB.
# `IWB=build/iw/a20/pl.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw272.py -n 25 -t 2`
import os
BASE = os.environ.get('IWB', 'build/iw/a20/pl.c')
H = '''	uint32_t off = imgSizeAligned();

	if (imgFits(off, len)) {
		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		nFsFiles++;
	} else {
		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
	}
'''
BODY = {
 'b0': '''		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
''',
 'b1': '''		blk = off >> 14;
		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
''',
 'b2': '''		f = &fsFiles[nFsFiles];
		f->block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		f->size = SWAP32_IMAGE_WRITE(len);
		strcpy(f->name, name);
		f->time = *time;
''',
 'b3': '''		f = fsFiles + nFsFiles;
		blk = off >> 14;
		f->block = SWAP16_IMAGE_WRITE(blk - xb.fsStart);
		f->size = SWAP32_IMAGE_WRITE(len);
		strcpy(f->name, name);
		f->time = *time;
''',
 'b4': '''		n = nFsFiles;
		fsFiles[n].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);
		fsFiles[n].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[n].name, name);
		fsFiles[n].time = *time;
''',
 'b5': '''		blk = (off >> 14) - xb.fsStart;
		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk);
		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
''',
}
CALL = {
 'c0': '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
''',
 'c1': '''		if (xb.bigBlock)
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		else
			imgAdd(off, data, len, 0, 0xffff, 1);
''',
 'c2': '''		imgAdd(off, data, len, xb.bigBlock ? 0x2a : 0, 0xffff, 1);
''',
 'c3': '''		if (!xb.bigBlock) {
			imgAdd(off, data, len, 0, 0xffff, 1);
			nFsFiles++;
			return;
		}
		imgAdd(off, data, len, 0x2a, 0xffff, 1);
''',
}
ENV = {
 'e0': lambda b, c: '	if (imgFits(off, len)) {\n' + b + c + '		nFsFiles++;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n	}\n',
 'e1': lambda b, c: '	if (!imgFits(off, len)) {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n		return;\n	}\n' + (b + c + '		nFsFiles++;\n').replace('\n\t\t', '\n\t').replace('\t\t', '\t', 1),
}
DL = {'d0': '	uint32_t off = imgSizeAligned();\n\n', 'd1': '	uint32_t off;\n\n	off = imgSizeAligned();\n'}
A = []
for dk, d in DL.items():
 for bk, b in BODY.items():
  for ck, c in CALL.items():
   for ek, e in ENV.items():
    v = ''
    if 'blk' in b: v += '	uint32_t blk;\n'
    if 'f->' in b: v += '	struct fsent *f;\n'
    if 'n = nFs' in b: v += '	int n;\n'
    dd = d.replace('\n\n', '\n' + v + '\n', 1) if v and dk == 'd0' else (d.replace('uint32_t off;\n\n', 'uint32_t off;\n' + v + '\n') if v else d)
    A.append(('%s_%s_%s_%s' % (dk, bk, ck, ek), [(H, dd + e(b, c))]))
AXES = [A]
