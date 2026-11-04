# attempt 10: pin_hdr gone.  Class u (mismatch 9%, first match): hdr/spare swapped because r197 (spare[12]'s saved byte) stays at pri 2; its mismatch reloads floor to REG_FREQ 0.
# Class v (no PRED_LOOP_EXIT on the mismatch, opcode's 72%): hdr right, pri 3, but pageErased 36.  Between them: the mismatch edge with no opcode prediction, 50%, or other spellings.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
HEAD = 'int pageErased(const uint8_t *data, const uint8_t *spare)\n{\n'
FLAG = '		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased'
FORMS = {
 # (parameter, body, call)
 'lt': ('int b', 'if (b < 0xff)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 'lt2': ('int b', 'if (b < 0xff)\n		return 0;\n	return 1;\n', '!byteOk(spare[i])'),
 'ge': ('int b', 'if (b >= 0xff)\n		return 0;\n	return 1;\n', 'byteUsed(spare[i])'),
 'ge2': ('int b', 'if (b >= 0xff)\n		return 1;\n	return 0;\n', '!byteOk(spare[i])'),
 'gt': ('int b', 'if (b > 0xfe)\n		return 0;\n	return 1;\n', 'byteUsed(spare[i])'),
 'le': ('int b', 'if (b <= 0xfe)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 'nz': ('uint8_t b', 'if ((uint8_t)~b)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 'nz2': ('uint8_t b', 'if ((uint8_t)~b)\n		return 0;\n	return 1;\n', '!byteOk(spare[i])'),
 'z': ('uint8_t b', 'if (!(uint8_t)~b)\n		return 0;\n	return 1;\n', 'byteUsed(spare[i])'),
 'z2': ('uint8_t b', 'if (!(uint8_t)~b)\n		return 1;\n	return 0;\n', '!byteOk(spare[i])'),
 'x': ('uint8_t b', 'if (b ^ 0xff)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 'x2': ('uint8_t b', 'if (b ^ 0xff)\n		return 0;\n	return 1;\n', '!byteOk(spare[i])'),
 'y': ('uint8_t b', 'if (!(b ^ 0xff))\n		return 0;\n	return 1;\n', 'byteUsed(spare[i])'),
 'y2': ('uint8_t b', 'if (!(b ^ 0xff))\n		return 1;\n	return 0;\n', '!byteOk(spare[i])'),
 'a': ('uint8_t b', 'if (b + 1 != 0x100)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 's': ('signed char b', 'if (b == -1)\n		return 0;\n	return 1;\n', 'byteUsed(spare[i])'),
 's2': ('signed char b', 'if (b != -1)\n		return 1;\n	return 0;\n', 'byteUsed(spare[i])'),
 's3': ('signed char b', 'if (b >= 0)\n		return 1;\n	return b != -1;\n', 'byteUsed(spare[i])'),
}
V = []
for k, (par, body, call) in FORMS.items():
    nm = 'byteOk' if 'byteOk' in call else 'byteUsed'
    V.append((k, [(HEAD, 'static int %s(%s)\n{\n	%s}\n\n' % (nm, par, body) + HEAD), (FLAG, FLAG.replace('spare[i] != 0xff', call))]))
AXES = [
 [('nopin', [(PIN, '')])],
 V,
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
