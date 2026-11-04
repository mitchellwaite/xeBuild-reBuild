# attempt 22: xmalloc by bit-CCP, part 2. M* are mechanism probes (not candidates): an empty byte-step loop that sccp resolves after ccp3, leaving memcpy calls alone.
# R* are real byte copies that ldist could turn back into memcpy, given restrict for its dependence test.
# `IWB=build/iw/a22/pm.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw283.py -n 40 -t 4`
MC = '''			memcpy(raw, h + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);
			raw += 528;
'''
HD = '			memcpy(raw, h + (b * 32 + p) * 512, 512);\n'
SP = '			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);\n'
FN = 'int finalizeImage(void)\n{'
CP = '''static uint8_t *copyBytes(uint8_t *restrict d, const uint8_t *restrict s, int n)
{
	while (n--)
		*d++ = *s++;
	return d;
}

'''
CP2 = '''static uint8_t *copyBytes(uint8_t *restrict d, const uint8_t *restrict s, int n)
{
	int i;

	for (i = 0; i < n; i++)
		*d++ = s[i];
	return d;
}

'''
AXES = [[
 ('base', []),
 ('M16', [(MC, HD + SP + '			{ int k; raw += 512; for (k = 0; k < 16; k++) raw++; }\n')]),
 ('M528', [(MC, HD + SP + '			{ int k; for (k = 0; k < 528; k++) raw++; }\n')]),
 ('M2', [(MC, HD + SP + '			raw += 526;\n			{ int k; for (k = 0; k < 2; k++) raw++; }\n')]),
 ('M4', [(MC, HD + SP + '			raw += 524;\n			{ int k; for (k = 0; k < 4; k++) raw++; }\n')]),
 ('R1', [(FN, CP + FN), (MC, HD + '			raw = copyBytes(raw + 512, q + (b * 32 + p) * 16, 16);\n')]),
 ('R2', [(FN, CP2 + FN), (MC, HD + '			raw = copyBytes(raw + 512, q + (b * 32 + p) * 16, 16);\n')]),
 ('R3', [(FN, CP + FN), (MC, '			raw = copyBytes(raw, h + (b * 32 + p) * 512, 512);\n			raw = copyBytes(raw, q + (b * 32 + p) * 16, 16);\n')]),
 ('R4', [(FN, CP2 + FN), (MC, '			raw = copyBytes(raw, h + (b * 32 + p) * 512, 512);\n			raw = copyBytes(raw, q + (b * 32 + p) * 16, 16);\n')]),
 ('R5', [(MC, HD + '			{ uint8_t *restrict d = raw + 512; const uint8_t *restrict e = q + (b * 32 + p) * 16; int k;\n			for (k = 0; k < 16; k++)\n				*d++ = e[k];\n			raw = d; }\n')]),
]]
