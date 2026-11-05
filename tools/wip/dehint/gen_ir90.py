"""getImageSmc with the hints it still needs for the address kept: attribute and shot gone, size tests nested on a second variable (51.8%).  Lattice of the other hints."""
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
DECL = '	int size = SWAP32(h->smcBootSize);\n'
HEAD = '''	if (size != 0x3000 && size != 0x3800) {
		shot: __attribute__((hot));
'''
PINE = '''	} else
		__asm__("" : "+D"(addr));
'''
PIN0 = '	}\n'
UN = '''			if (!h)
				__builtin_unreachable();
'''
V = '''	} else {
		vhot: __attribute__((hot));
	}
'''
B = '	bhot: __attribute__((hot));\n'
E1 = 'if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'
A0 = [('', [(ATTR, 'void getImageSmc')])]
AS = [
    ('s2n', [(DECL, '	int s = SWAP32(h->smcBootSize);\n	uint32_t size = s;\n'),
             (HEAD, '	if (s != 0x3000) {\n	if (s != 0x3800) {\n'), (PINE, '	}\n' + PINE)]),
    ('s3n', [(DECL, '	uint32_t s = SWAP32(h->smcBootSize);\n	int size = s;\n'),
             (HEAD, '	if (s != 0x3000) {\n	if (s != 0x3800) {\n'), (PINE, '	}\n' + PINE)]),
    ('s2p', [(DECL, '	int s = SWAP32(h->smcBootSize);\n	uint32_t size = s;\n'),
             (HEAD, '	if (s != 0x3000) {\n	if (s != 0x3800) {\n'), (PINE, '	}\n	}\n')]),
    ('s3p', [(DECL, '	uint32_t s = SWAP32(h->smcBootSize);\n	int size = s;\n'),
             (HEAD, '	if (s != 0x3000) {\n	if (s != 0x3800) {\n'), (PINE, '	}\n	}\n')]),
]
AU = [('uk', []), ('u0', [(UN, '')])]
AV = [('vk', []), ('v0', [(V, '	}\n')])]
AB = [('bk', []), ('b0', [(B, '')])]
AE = [('ek', []), ('e0', [(E1, 'if (addr < 528 * xb.dumpPages) {')])]
AXES = [A0, AS, AU, AV, AB, AE]
