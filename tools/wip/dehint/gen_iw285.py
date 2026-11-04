# attempt 22: spellings of gen_iw284's T1 (the page's two parts copied by a loop over a size table), plain malloc.
# `IWB=build/iw/a22/pm.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw285.py -n 40 -t 4`
MC = '''			memcpy(raw, h + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);
			raw += 528;
'''
FN = 'int finalizeImage(void)\n{'
TB = 'static const uint32_t pageParts[2] = { 512, 16 };\n\n'
H = 'h + (b * 32 + p) * 512'
Q = 'q + (b * 32 + p) * 16'
ASG = '			{ const uint8_t *from[2]; int k;\n			from[0] = %s;\n			from[1] = %s;\n' % (H, Q)
INI = '			{ const uint8_t *from[2] = { %s, %s }; int k;\n' % (H, Q)
LOOP = '			for (k = 0; k < 2; k++) {\n				memcpy(raw, from[k], SZ[k]);\n				raw += SZ[k];\n			} }\n'
def L(sz): return LOOP.replace('SZ', sz)
AXES = [[
 ('filestatic', [(FN, TB + FN), (MC, ASG + L('pageParts'))]),
 ('fileinit', [(FN, TB + FN), (MC, INI + L('pageParts'))]),
 ('fnstatic', [(MC, '			{ static const uint32_t size[2] = { 512, 16 };\n' + INI.replace('{ const', 'const', 1) + L('size'))]),
 ('fnstatictop', [('	uint8_t *raw, *s, *spare;\n	void *mem;\n', '	uint8_t *raw, *s, *spare;\n	void *mem;\n	static const uint32_t size[2] = { 512, 16 };\n'), (MC, INI + L('size'))]),
 ('localconst', [(MC, '			{ const uint32_t size[2] = { 512, 16 };\n' + INI.replace('{ const', 'const', 1) + L('size'))]),
 ('localplain', [(MC, '			{ uint32_t size[2] = { 512, 16 };\n' + INI.replace('{ const', 'const', 1) + L('size'))]),
 ('struct', [(MC, '			{ const struct { const uint8_t *from; uint32_t size; } part[2] = { { %s, 512 }, { %s, 16 } }; int k;\n			for (k = 0; k < 2; k++) {\n				memcpy(raw, part[k].from, part[k].size);\n				raw += part[k].size;\n			} }\n' % (H, Q))]),
 ('unsignedk', [(FN, TB + FN), (MC, INI.replace('int k', 'uint32_t k') + L('pageParts'))]),
 ('filestatic_n', [(FN, TB + FN), (MC, INI.replace(' int k;', '') + LOOP.replace('k', 'n').replace('SZ', 'pageParts'))]),
]]
