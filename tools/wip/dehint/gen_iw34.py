# attempt 3: xmalloc/pin_hdr. finalizeImage's raw image pointer not as a `raw` iv from mem: ivopts' new iv has no alignment info.
FOCUS = ['_finalizeImage']
X = '''void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n'''
A = 'xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));'
L = '''	raw = (uint8_t *)mem;
	for (b = 0; b < xb.blocks; b++)
		for (p = 0; p < 32; p++) {
			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
		}
'''
def loop(pre, d1, d2, post='', pin=True, inner=''):
    return ('	' + pre + '''for (b = 0; b < xb.blocks; b++)
		for (p = 0; p < 32; p++) {
			''' + inner + '''if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
''' + ('			__asm__("" :: "a"(xb.hdr));\n' if pin else '') +
    '			memcpy(' + d1 + ', xb.hdr + (b * 32 + p) * 512, 512);\n'
    '			memcpy(' + d2 + ', xb.spare + (b * 32 + p) * 16, 16);\n' + post + '		}\n')
OFF = 'uint32_t o = 0;\n	'
forms = []
for pin in (True, False):
    tag = 'P' if pin else 'N'
    forms += [
        ('idx' + tag, [(L, loop('', '(uint8_t *)mem + (b * 32 + p) * 528', '(uint8_t *)mem + (b * 32 + p) * 528 + 512', pin=pin))]),
        ('idx2' + tag, [(L, loop('', '(uint8_t *)mem + (b * 32 + p) * 528', '(uint8_t *)mem + (b * 32 + p) * 512 + (b * 32 + p) * 16 + 512', pin=pin))]),
        ('off' + tag, [(L, loop('{ ' + OFF, '(uint8_t *)mem + o', '(uint8_t *)mem + o + 512', '			o += 528;\n', pin=pin) + '	}\n')]),
        ('blk' + tag, [(L, loop('', 'raw + p * 528', 'raw + p * 528 + 512', pin=pin, inner='raw = (uint8_t *)mem + b * 0x4200;\n			'))]),
        ('raw' + tag, [(L, L if pin else L.replace('			__asm__("" :: "a"(xb.hdr));\n', ''))]),
    ]
AXES = [
    [('xm', []), ('nox', [(X, ''), ('xmalloc(xb.rawSize)', 'malloc(xb.rawSize)')])],
    forms,
]
