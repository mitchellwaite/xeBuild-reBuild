# attempt 22: xmalloc by bit-CCP. CCP's ALIGN comes from the lattice's known low bits, so a byte-stepped pointer loses it on raw's PHI, and sccp (after ccp3)
# can then turn the byte loop's exit value back into a constant step. The spare copy as a byte loop, plain malloc.
# `IWB=build/iw/a22/pm.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw282.py -n 40 -t 4`
MC = '''			memcpy(raw, h + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, q + (b * 32 + p) * 16, 16);
			raw += 528;
'''
HD = '			memcpy(raw, h + (b * 32 + p) * 512, 512);\n'
SP = 'q + (b * 32 + p) * 16'
AXES = [[
 ('base', []),
 ('a', [(MC, HD + '			raw += 512;\n			q += (b * 32 + p) * 16;\n			for (n = 0; n < 16; n++)\n				*raw++ = q[n];\n')]),
 ('b', [(MC, HD + '			raw += 512;\n			q += (b * 32 + p) * 16;\n			for (n = 0; n < 16; n++)\n				*raw++ = *q++;\n')]),
 ('c', [(MC, HD + '			raw += 512;\n			{ int k;\n			q += (b * 32 + p) * 16;\n			for (k = 0; k < 16; k++)\n				*raw++ = q[k]; }\n')]),
 ('d', [(MC, HD + '			raw += 512;\n			{ int k;\n			for (k = 0; k < 16; k++)\n				raw[k] = q[(b * 32 + p) * 16 + k]; }\n			raw += 16;\n')]),
 ('e', [(MC, HD + '			raw += 512;\n			{ int k;\n			for (k = 0; k < 16; k++)\n				*raw++ = q[(b * 32 + p) * 16 + k]; }\n')]),
 ('f', [(MC, '			{ int k;\n			for (k = 0; k < 512; k++)\n				*raw++ = h[(b * 32 + p) * 512 + k]; }\n			memcpy(raw, ' + SP + ', 16);\n			raw += 16;\n')]),
]]
