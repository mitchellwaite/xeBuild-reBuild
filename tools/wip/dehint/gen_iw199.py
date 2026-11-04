# attempt 13: xmalloc. The Linux build's ECC loop resets its output pointer once per block (rbx += 0x4200; r8 = rbx) and
# has the same unaligned-dest memcpy with a builtin malloc, so the pointer may not be one incrementing `raw`: ivopts' new IV
# carries no alignment. Forms of the output pointer, plain malloc.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/s_nohdr.c')
XM = 'void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n'
AL = 'xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));'
MC = '''			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
'''
RI = '	raw = (uint8_t *)mem;\n'
H = 'xb.hdr + (b * 32 + p) * 512'
S = 'xb.spare + (b * 32 + p) * 16'
def F(body, ri=RI):
    return [(MC, body), (RI, ri)]
A = [
 ('r0', F(MC)),
 ('r1', F('			memcpy((uint8_t *)mem + (b * 32 + p) * 528, %s, 512);\n			memcpy((uint8_t *)mem + (b * 32 + p) * 528 + 512, %s, 16);\n' % (H, S), '')),
 ('r2', F('			raw = (uint8_t *)mem + (b * 32 + p) * 528;\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (H, S), '')),
 ('r3', F('			raw = (uint8_t *)mem + b * 0x4200 + p * 528;\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (H, S), '')),
 ('r4', F('			memcpy((uint8_t *)mem + b * 0x4200 + p * 528, %s, 512);\n			memcpy((uint8_t *)mem + b * 0x4200 + p * 528 + 512, %s, 16);\n' % (H, S), '')),
 ('r5', F('			memcpy((uint8_t *)mem + (b * 32 + p) * 512 + (b * 32 + p) * 16, %s, 512);\n			memcpy((uint8_t *)mem + (b * 32 + p) * 512 + (b * 32 + p) * 16 + 512, %s, 16);\n' % (H, S), '')),
 ('r6', F('			raw = (uint8_t *)mem + b * 0x4200;\n			memcpy(raw + p * 528, %s, 512);\n			memcpy(raw + p * 528 + 512, %s, 16);\n' % (H, S), '')),
 ('r7', F('			memcpy(&((uint8_t *)mem)[(b * 32 + p) * 528], %s, 512);\n			memcpy(&((uint8_t *)mem)[(b * 32 + p) * 528 + 512], %s, 16);\n' % (H, S), '')),
 ('r8', F('			{ uint32_t o = (b * 32 + p) * 528;\n			memcpy((uint8_t *)mem + o, %s, 512);\n			memcpy((uint8_t *)mem + o + 512, %s, 16); }\n' % (H, S), '')),
 ('r9', F('			memcpy(raw, %s, 512);\n			raw += 512;\n			memcpy(raw, %s, 16);\n			raw += 16;\n' % (H, S))),
]
AXES = [[('m', [(XM, ''), (AL, 'xb.raw = (uint8_t *)(mem = malloc(xb.rawSize));')])], A]
FLAGS = []
