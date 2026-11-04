# attempt 10: on drafts/image_write_near10.c.  blockEccOk's 18 comes from a forwarder block holding the spare[12] PHI (bb49 in optimized; in the reference the PHI sits in bb11), left by threading
# through the byte helper's test.  Forms of the spare loop's exit and of where the helper is used: pageErased directly or through spareUsed.
import os
L = '''	for (i = 0; i < 16; i++)
		if (byteUsed(spare[i]))
			return 0;
	return 1;
}

int blockErased'''
SU = '''	for (i = 0; i < 16; i++)
		if (s[i] != 0xff)
			return 1;
	return 0;
}

uint8_t *imageGetBuffer'''
HELP = 'static int byteUsed(uint8_t b)\n{\n	if (b != 0xff)\n		return 1;\n	return 0;\n}\n\n'
HEAD = 'int pageErased(const uint8_t *data, const uint8_t *spare)\n{\n'
SUU = SU.replace('s[i] != 0xff', 'byteUsed(s[i])')
F = {
 '': [],
 'a': [(L, '	for (i = 0; i < 16; i++)\n		if (byteUsed(spare[i]))\n			break;\n	if (i == 16)\n		return 1;\n	return 0;\n}\n\nint blockErased')],
 'b': [(L, '	for (i = 0; i < 16; i++)\n		if (byteUsed(spare[i]))\n			break;\n	return i == 16;\n}\n\nint blockErased')],
 'c': [(L, '	for (i = 0; i < 16; i++)\n		if (byteUsed(spare[i]))\n			break;\n	if (i < 16)\n		return 0;\n	return 1;\n}\n\nint blockErased')],
 'd': [(L, '	for (i = 0; i < 16; i++) {\n		int used = byteUsed(spare[i]);\n\n		if (used)\n			return 0;\n	}\n	return 1;\n}\n\nint blockErased')],
 'e': [(L, '	for (i = 0; i < 16; i++) {\n		if (!byteUsed(spare[i]))\n			continue;\n		return 0;\n	}\n	return 1;\n}\n\nint blockErased')],
 'f': [(L, '	for (i = 0; i < 16; i++) {\n		if (byteUsed(spare[i]) != 0)\n			return 0;\n	}\n	return 1;\n}\n\nint blockErased')],
 'g': [(L, '	for (i = 0; i < 16; i++) {\n		if (byteUsed(spare[i]) == 1)\n			return 0;\n	}\n	return 1;\n}\n\nint blockErased')],
 'h': [(L, '	for (i = 0; i < 16; i++) {\n		if (byteUsed(spare[i]) > 0)\n			return 0;\n	}\n	return 1;\n}\n\nint blockErased')],
 's1': [(L, '	return !spareUsed(spare);\n}\n\nint blockErased'), (SU, SUU)],
 's2': [(L, '	if (spareUsed(spare))\n		return 0;\n	return 1;\n}\n\nint blockErased'), (SU, SUU)],
 's3': [(L, '	if (!spareUsed(spare))\n		return 1;\n	return 0;\n}\n\nint blockErased'), (SU, SUU)],
 's4': [(L, '	return spareUsed(spare) == 0;\n}\n\nint blockErased'), (SU, SUU)],
}
AXES = [[(k, v) for k, v in F.items()]]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near10.c')
FLAGS = []
