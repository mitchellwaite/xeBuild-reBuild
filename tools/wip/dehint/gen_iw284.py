# attempt 22: xmalloc by bit-CCP, part 3: real reasons for raw's step to be unknown at ccp3 and constant later. Table of section sizes, a page size summed by a loop, a static never written, helpers.
# `IWB=build/iw/a22/pm.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw284.py -n 40 -t 4`
MC = '''			memcpy(raw, h + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);
			raw += 528;
'''
HD = '			memcpy(raw, h + (b * 32 + p) * 512, 512);\n'
SP = '			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);\n'
FN = 'int finalizeImage(void)\n{'
TB = 'static const uint32_t pageParts[2] = { 512, 16 };\n\n'
ST = 'static uint32_t pageSize = 528;\n\n'
RI = '	raw = (uint8_t *)mem;\n'
AXES = [[
 ('T1', [(FN, TB + FN), (MC, '			{ const uint8_t *from[2]; int k;\n			from[0] = h + (b * 32 + p) * 512;\n			from[1] = q + (b * 32 + p) * 16;\n			for (k = 0; k < 2; k++) {\n				memcpy(raw, from[k], pageParts[k]);\n				raw += pageParts[k];\n			} }\n')]),
 ('T2', [(FN, TB + FN), (MC, '			{ int k;\n			for (k = 0; k < 2; k++) {\n				memcpy(raw, k ? q + (b * 32 + p) * 16 : h + (b * 32 + p) * 512, k ? 16 : 512);\n				raw += k ? 16 : 512;\n			} }\n')]),
 ('T3', [(FN, TB + FN), (MC, HD + SP + '			{ int k;\n			for (k = 0; k < 2; k++)\n				raw += pageParts[k]; }\n')]),
 ('T4', [(FN, TB + FN), (RI, RI + '	{ int k;\n	for (n = 0, k = 0; k < 2; k++)\n		n += pageParts[k]; }\n'), (MC, HD + SP + '			raw += n;\n')]),
 ('T5', [(FN, ST + FN), (MC, HD + SP + '			raw += pageSize;\n')]),
 ('T6', [(MC, HD + SP + '			{ int k;\n			for (k = 0; k < 2; k++)\n				raw += k ? 16 : 512; }\n')]),
 ('T7', [(RI, RI + '	{ uint32_t k;\n	for (n = 0, k = 1; k <= 33; k++)\n		n += 16; }\n'), (MC, HD + SP + '			raw += n;\n')]),
 ('T8', [(RI, RI + '	{ uint32_t k;\n	for (n = 0, k = 0; k < 528; k++)\n		n++; }\n'), (MC, HD + SP + '			raw += n;\n')]),
 ('T9', [(MC, HD + SP + '			{ uint32_t k;\n			for (k = 512; k > 0; k >>= 1)\n				if (k == 16 || k == 512) raw += k; }\n')]),
]]
