# attempt 18: xmalloc. Plain malloc; forms of the ECD loop's output pointer not tried by gen_iw199: real per-block pointers (Linux keeps rbx += 0x4200, r8 = rbx) and page structs.
# `iw16sweep.py tools/wip/dehint/gen_iw251.py -n 40`, IWB = src by default. Any state with the prologue has ~2 lines of finalizeImage's memcpy right.
import os
BASE = os.environ.get('IWB', 'src/image_write.c')
XM = 'void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n'
AL = 'xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));'
PLAIN = [(XM, ''), (AL, 'xb.raw = (uint8_t *)(mem = malloc(xb.rawSize));')]
MC = '''			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
'''
RI = '	raw = (uint8_t *)mem;\n'
LOOP = '''	for (b = 0; b < xb.blocks; b++)
		for (p = 0; p < 32; p++) {
			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
''' + MC + '		}\n'
H = 'xb.hdr + (b * 32 + p) * 512'
S = 'xb.spare + (b * 32 + p) * 16'
HEAD = '''	for (b = 0; b < xb.blocks; b++) %s
		for (p = 0; p < 32; p++) {
			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
'''
ST = 'struct rawpage { uint8_t data[512]; uint8_t spare[16]; };\n\nint finalizeImage(void)\n'
SD = 'int finalizeImage(void)\n'
PB = '''	{
		uint8_t *bp = (uint8_t *)mem;

	for (b = 0; b < xb.blocks; b++) {
		raw = bp;
		for (p = 0; p < 32; p++) {
			if (!pageErased(%s, %s))
				calcPageEcc(%s, %s);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, %s, 512);
			memcpy(raw + 512, %s, 16);
			raw += 528;
		}
		bp += 0x4200;
	}
	}
''' % (H, S, H, S, H, S)
def body(mc, pre='', ri=''):
    return [(LOOP, HEAD % '' + mc + '		}\n'), (RI, ri)] + pre
A = [('r0', []),
 ('bp', [(LOOP, PB), (RI, '')]),
 ('pgp', body('			memcpy(pg->data, %s, 512);\n			memcpy(pg->spare, %s, 16);\n			pg++;\n' % (H, S), [(SD, ST)], '	{ struct rawpage *pg = mem;\n')),
]
A = [('r0', []), ('bp', [(LOOP, PB), (RI, '')])]
def st(mc, ri):
    return [(LOOP, ri + HEAD % '' + mc + '		}\n	}\n'), (RI, ''), (SD, ST)]
A += [
 ('pgp', st('			memcpy(pg->data, %s, 512);\n			memcpy(pg->spare, %s, 16);\n			pg++;\n' % (H, S), '	{\n	struct rawpage *pg = mem;\n')),
 ('pga', st('			memcpy(pg[b * 32 + p].data, %s, 512);\n			memcpy(pg[b * 32 + p].spare, %s, 16);\n' % (H, S), '	{\n	struct rawpage *pg = mem;\n')),
 ('pgb', st('			memcpy(((struct rawpage *)mem)[b * 32 + p].data, %s, 512);\n			memcpy(((struct rawpage *)mem)[b * 32 + p].spare, %s, 16);\n' % (H, S), '	{\n')),
 ('pgc', st('			{ struct rawpage *pg = (struct rawpage *)mem + b * 32 + p;\n			memcpy(pg->data, %s, 512);\n			memcpy(pg->spare, %s, 16); }\n' % (H, S), '	{\n')),
 ('pgd', st('			memcpy(&pg->data, %s, 512);\n			memcpy(&pg->spare, %s, 16);\n			pg++;\n' % (H, S), '	{\n	struct rawpage *pg = mem;\n')),
]
AXES = [[('m', PLAIN)], A]
FLAGS = []
# 2D forms: Linux has rbx (mem + b * 0x4200) and r8 (rbx + p * 0x210) as 64-bit IVs next to 32-bit b and p, which reads as array indexing: the index widens before the multiply
ST2 = 'struct rawpage { uint8_t data[512]; uint8_t spare[16]; };\nstruct rawblock { struct rawpage page[32]; };\n\nint finalizeImage(void)\n'
def st2(mc, ri):
    return [(LOOP, ri + HEAD % '' + mc + '		}\n	}\n'), (RI, ''), (SD, ST2)]
A = [
 ('d2a', st2('			memcpy(rb[b].page[p].data, %s, 512);\n			memcpy(rb[b].page[p].spare, %s, 16);\n' % (H, S), '	{\n	struct rawblock *rb = mem;\n')),
 ('d2b', st2('			{ struct rawpage *pg = &rb[b].page[p];\n			memcpy(pg->data, %s, 512);\n			memcpy(pg->spare, %s, 16); }\n' % (H, S), '	{\n	struct rawblock *rb = mem;\n')),
 ('d2c', st2('			memcpy(rb[b][p], %s, 512);\n			memcpy(&rb[b][p][512], %s, 16);\n' % (H, S), '	{\n	uint8_t (*rb)[32][528] = mem;\n')),
 ('d2d', st2('			memcpy(rb[b][p], %s, 512);\n			memcpy(rb[b][p] + 512, %s, 16);\n' % (H, S), '	{\n	uint8_t (*rb)[32][528] = mem;\n')),
 ('d2e', st2('			memcpy(&rb[b].page[p], %s, 512);\n			memcpy(&rb[b].page[p].spare, %s, 16);\n' % (H, S), '	{\n	struct rawblock *rb = mem;\n')),
 ('d2f', st2('			memcpy(rb[b * 32 + p], %s, 512);\n			memcpy(rb[b * 32 + p] + 512, %s, 16);\n' % (H, S), '	{\n	uint8_t (*rb)[528] = mem;\n')),
 ('d2g', st2('			memcpy(rb[b] + p * 528, %s, 512);\n			memcpy(rb[b] + p * 528 + 512, %s, 16);\n' % (H, S), '	{\n	uint8_t (*rb)[0x4200] = mem;\n')),
 ('d2h', st2('			memcpy(&rb[b][p * 528], %s, 512);\n			memcpy(&rb[b][p * 528 + 512], %s, 16);\n' % (H, S), '	{\n	uint8_t (*rb)[0x4200] = mem;\n')),
]
AXES = [[('m', PLAIN)], A]
