# attempt 10: on build/iw/a10/c_sa.c (byte helper + gen_iw174 `sa`, no pin, no expect): blockEccOk 18, finalizeImage 8 (preheader loads, MU loop's compare).
# blockEccOk's forms and the MU compare's forms.
import os
BE = '''	for (i = 0; i < pages; i++) {
		if (pageErased(blk + i * 528, blk + i * 528 + 512))
			continue;
		if (pageEccOk(blk + i * 528, blk + i * 528 + 512))
			continue;
		return 0;
	}
	return 1;
'''
A = 'blk + i * 528, blk + i * 528 + 512'
BF = {
 '': BE,
 'b1': f'	for (i = 0; i < pages; i++)\n		if (!pageErased({A}) && !pageEccOk({A}))\n			return 0;\n	return 1;\n',
 'b2': f'	for (i = 0; i < pages; i++) {{\n		if (!pageErased({A})) {{\n			if (!pageEccOk({A}))\n				return 0;\n		}}\n	}}\n	return 1;\n',
 'b3': f'	for (i = 0; i < pages; i++) {{\n		if (pageErased({A}))\n			continue;\n		if (!pageEccOk({A}))\n			return 0;\n	}}\n	return 1;\n',
 'b4': f'	for (i = 0; i < pages; i++) {{\n		if (pageErased({A}) || pageEccOk({A}))\n			continue;\n		return 0;\n	}}\n	return 1;\n',
 'b5': f'	for (i = 0; i < pages; i++) {{\n		if (!pageErased({A}))\n			if (!pageEccOk({A}))\n				return 0;\n	}}\n	return 1;\n',
 'b6': f'	for (i = 0; i < pages; i++) {{\n		uint8_t *d = blk + i * 528;\n\n		if (pageErased(d, d + 512))\n			continue;\n		if (pageEccOk(d, d + 512))\n			continue;\n		return 0;\n	}}\n	return 1;\n',
 'b7': f'	for (i = 0; i < pages; i++) {{\n		uint8_t *d = blk + i * 528, *s = d + 512;\n\n		if (pageErased(d, s))\n			continue;\n		if (pageEccOk(d, s))\n			continue;\n		return 0;\n	}}\n	return 1;\n',
 'b8': f'	for (i = 0; i < pages; i++) {{\n		if (pageErased({A}))\n			continue;\n		if (pageEccOk({A}) == 0)\n			return 0;\n	}}\n	return 1;\n',
}
MU = '		for (b = xb.spare7; b < xb.muBlocks; b++)\n			for (p = 0; p < 256; p++) {\n				memcpy(raw, xb.dump'
MF = {
 '': MU,
 'm1': MU.replace('b < xb.muBlocks', 'xb.muBlocks > b'),
 'm2': MU.replace('for (b = xb.spare7; b < xb.muBlocks; b++)', 'for (b = xb.spare7; b != xb.muBlocks; b++)'),
}
AXES = [
 [(k, [(BE, v)]) for k, v in BF.items()],
 [(k, [(MU, v)]) for k, v in MF.items()],
]
BASE = os.environ.get('IWB', 'build/iw/a10/c_sa.c')
FLAGS = []
