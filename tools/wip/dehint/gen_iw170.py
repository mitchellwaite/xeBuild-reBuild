# attempt 10: pin_hdr (A).  predict_extra_loop_exits: an exit test on a PHI of constants puts PRED_LOOP_EXIT 9% (hitrate 91, not divided by n_exits) on the edge into the PHI.  So a byte
# test that goes through a helper written with `if` (the imgFits lesson: no early phiopt, the PHI of 1 and 0 survives early inlining) should get 9% per byte instead of 4.5%, in the
# spare window of 5-15%.  Good: finalizeImage 57 and nothing else.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
HEAD = 'int pageErased(const uint8_t *data, const uint8_t *spare)\n{\n'
DT = '		if (data[i] != 0xff)\n			return 0;\n	for (i = 0; i < 16; i++)\n		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased'
H = {
 'u': ('static int byteUsed(uint8_t b)\n{\n	if (b != 0xff)\n		return 1;\n	return 0;\n}\n\n', 'byteUsed(%s)'),
 'e': ('static int byteErased(uint8_t b)\n{\n	if (b == 0xff)\n		return 1;\n	return 0;\n}\n\n', '!byteErased(%s)'),
 'v': ('static int byteUsed(uint8_t b)\n{\n	if (b == 0xff)\n		return 0;\n	return 1;\n}\n\n', 'byteUsed(%s)'),
 'n': ('static int byteErased(uint8_t b)\n{\n	if (b != 0xff)\n		return 0;\n	return 1;\n}\n\n', '!byteErased(%s)'),
 'r': ('static int byteUsed(uint8_t b)\n{\n	return b != 0xff;\n}\n\n', 'byteUsed(%s)'),
}
def var(hk, wd, ws):
    h, c = H[hk]
    d = c % 'data[i]' if wd else 'data[i] != 0xff'
    s = c % 'spare[i]' if ws else 'spare[i] != 0xff'
    return [(HEAD, h + HEAD), (DT, DT.replace('data[i] != 0xff', d).replace('spare[i] != 0xff', s))]
FLAG = '		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased'
V = [(hk + w, var(hk, 'd' in w, 's' in w)) for hk in H for w in ('s', 'd', 'ds')]
V += [
 ('fl1', [('	int i;\n\n	for (i = 0; i < 512; i++)\n		if (data[i]', '	int i, used;\n\n	for (i = 0; i < 512; i++)\n		if (data[i]'),
          (FLAG, '	{\n		used = 0;\n		if (spare[i] != 0xff)\n			used = 1;\n		if (used)\n			return 0;\n	}\n	return 1;\n}\n\nint blockErased')]),
]
AXES = [
 [('nopin', [(PIN, '')])],
 V,
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
