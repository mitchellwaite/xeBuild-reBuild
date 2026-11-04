# attempt 8: xmalloc removed: forms of finalizeImage's raw pointer in the ECD loop (other tricks kept).
# Does any form lose the alignment so that the memcpy gets its prologue?  Look at _finalizeImage's lines (178 = no prologue, plain raw).
FLAGS = []
FOCUS = ['_finalizeImage']
BASE = 'build/iw/a8/nox.c'
HDR = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
'''
L = '''	raw = (uint8_t *)mem;
	for (b = 0; b < xb.blocks; b++)
		for (p = 0; p < 32; p++) {
''' + HDR + '''			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
		}
'''
D = 'xb.hdr + (b * 32 + p) * 512'
S = 'xb.spare + (b * 32 + p) * 16'
HEAD = '	for (b = 0; b < xb.blocks; b++)\n		for (p = 0; p < 32; p++) {\n' + HDR


def f(pre, body, post=''):
    return pre + HEAD + body + '		}\n' + post


FORMS = [
 ('base', []),
 ('split', [(L, '	raw = (uint8_t *)mem;\n' + f('', '			memcpy(raw, %s, 512);\n			raw += 512;\n			memcpy(raw, %s, 16);\n			raw += 16;\n' % (D, S)))]),
 ('post', [(L, '	raw = (uint8_t *)mem;\n' + f('', '			raw += 528;\n			memcpy(raw - 528, %s, 512);\n			memcpy(raw - 16, %s, 16);\n' % (D, S)))]),
 ('post2', [(L, '	raw = (uint8_t *)mem;\n' + f('', '			uint8_t *pg = raw;\n			raw += 528;\n			memcpy(pg, %s, 512);\n			memcpy(pg + 512, %s, 16);\n' % (D, S)))]),
 ('idx', [(L, f('', '			memcpy((uint8_t *)mem + (b * 32 + p) * 528, %s, 512);\n			memcpy((uint8_t *)mem + (b * 32 + p) * 528 + 512, %s, 16);\n' % (D, S)))]),
 ('idx2', [(L, f('', '			raw = (uint8_t *)mem + (b * 32 + p) * 528;\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (D, S)))]),
 ('idx3', [(L, f('', '			raw = (uint8_t *)mem + b * 0x4200 + p * 528;\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (D, S)))]),
 ('off', [(L, '	{ uint32_t o = 0;\n' + f('', '			memcpy((uint8_t *)mem + o, %s, 512);\n			memcpy((uint8_t *)mem + o + 512, %s, 16);\n			o += 528;\n' % (D, S)) + '	}\n')]),
 ('off2', [(L, '	{ uint32_t o = 0;\n' + f('', '			raw = (uint8_t *)mem + o;\n			o += 528;\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (D, S)) + '	}\n')]),
 ('blk', [(L, f('', '			raw = (uint8_t *)mem + b * 0x4200;\n			memcpy(raw + p * 528, %s, 512);\n			memcpy(raw + p * 528 + 512, %s, 16);\n' % (D, S)))]),
 ('blk2', [(L, '	for (b = 0; b < xb.blocks; b++) {\n		uint8_t *bp = (uint8_t *)mem + b * 0x4200;\n		for (p = 0; p < 32; p++) {\n' + HDR + '			memcpy(bp, %s, 512);\n			memcpy(bp + 512, %s, 16);\n			bp += 528;\n		}\n	}\n' % (D, S))]),
 ('blk3', [(L, '	for (b = 0; b < xb.blocks; b++) {\n		uint8_t *bp = (uint8_t *)mem + b * 0x4200;\n		for (p = 0; p < 32; p++) {\n' + HDR + '			memcpy(bp + p * 528, %s, 512);\n			memcpy(bp + p * 528 + 512, %s, 16);\n		}\n	}\n' % (D, S))]),
 ('st', [(L, '	{ struct rawpage { uint8_t data[512]; uint8_t spare[16]; } *rp = mem;\n' + f('', '			memcpy(rp->data, %s, 512);\n			memcpy(rp->spare, %s, 16);\n			rp++;\n' % (D, S)) + '	}\n')]),
 ('st2', [(L, '	{ struct rawpage { uint8_t data[512]; uint8_t spare[16]; } *rp = mem;\n' + f('', '			memcpy(rp[b * 32 + p].data, %s, 512);\n			memcpy(rp[b * 32 + p].spare, %s, 16);\n' % (D, S)) + '	}\n')]),
 ('arr', [(L, '	{ uint8_t (*rp)[528] = mem;\n' + f('', '			memcpy(*rp, %s, 512);\n			memcpy(*rp + 512, %s, 16);\n			rp++;\n' % (D, S)) + '	}\n')]),
 ('arr2', [(L, '	{ uint8_t (*rp)[528] = mem;\n' + f('', '			memcpy(rp[b * 32 + p], %s, 512);\n			memcpy(rp[b * 32 + p] + 512, %s, 16);\n' % (D, S)) + '	}\n')]),
]
AXES = [FORMS]
