# attempt 9: pin_hdr gone.  Forms of calcEcd and calcPageEcc: with the pin removed r187 (v) and r192 (data) take esi/edi the wrong way round,
# a margin that flips at head block freq >= 350 (expect 72-77).  Do any forms flip it at freq 345?  Good = finalizeImage about 53 lines
# (only the hdr/spare swap left, build/iw/a9/ex.c at -p 75 shows that diff).  All forms must leave calcEcd itself byte-equal.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
CE = '''	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;
	for (i = 0; i < 0x1066; i++) {
		if (!(i & 31)) {
			if (i == 0x1000)
				data = (unsigned int *)spare;
			v = ~*data++;
		}
		val ^= v & 1;
		v >>= 1;
		if (val & 1)
			val ^= 0x6954559;
		val >>= 1;
	}
	return ~val;
'''
def body(decl, head, read, mix, tail='	return ~val;\n'):
    return decl + '	for (i = 0; i < 0x1066; i++) {\n' + head + read + '		}\n' + mix + '	}\n' + tail
D0 = '''	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;
'''
D1 = '''	unsigned int *data = (unsigned int *)datc;
	unsigned int v = 0;
	unsigned int val = 0;
	unsigned int i;

'''
H0 = '''		if (!(i & 31)) {
			if (i == 0x1000)
				data = (unsigned int *)spare;
'''
H1 = '''		if ((i & 31) == 0) {
			if (i == 0x1000)
				data = (unsigned int *)spare;
'''
R0 = '			v = ~*data++;\n'
R1 = '			v = ~*data;\n			data++;\n'
R2 = '			v = *data++;\n			v = ~v;\n'
M0 = '''		val ^= v & 1;
		v >>= 1;
		if (val & 1)
			val ^= 0x6954559;
		val >>= 1;
'''
M1 = '''		val ^= v & 1;
		if (val & 1)
			val ^= 0x6954559;
		v >>= 1;
		val >>= 1;
'''
M2 = '''		val = (val ^ v) & 1 ? val ^ 0x6954559 : val;
		v >>= 1;
		val >>= 1;
'''
M3 = '''		val ^= v & 1;
		v >>= 1;
		val = val & 1 ? (val ^ 0x6954559) >> 1 : val >> 1;
'''
PC = '''	uint32_t val = calcEcd((uint8_t *)data, spare);

	spare[12] = (spare[12] & 0x3f) + (val << 6);
'''
PC1 = '''	uint8_t b = spare[12] & 0x3f;
	uint32_t val = calcEcd((uint8_t *)data, spare);

	spare[12] = b + (val << 6);
'''
AXES = [
 [('', [(PIN, '')])],
 [('', []), ('d1', [(D0 + '	for', D1 + '	for')])] ,
 [('', [])] + [('h1', [(H0, H1)])],
 [('', [])] + [('r1', [(R0, R1)]), ('r2', [(R0, R2)])],
 [('', [])] + [('m1', [(M0, M1)]), ('m2', [(M0, M2)]), ('m3', [(M0, M3)])],
 [('', []), ('pc1', [(PC, PC1)])],
]
FLAGS = []
FOCUS = ['_finalizeImage', '_calcEcd', '_calcPageEcc']
