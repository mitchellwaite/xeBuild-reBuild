# attempt 17: sccp splits loop exits whose dest has other preds (bb25->14, bb53->51 for the FS loops, because of the `blocks != 0` guard), each split taking one .MEM PHI name.
# do-while for i and/or b removes the guard. On IWB (src minus optimize), x dead test on/off.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/na.c')
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
F0 = '		for (i = 0; i < blocks; i++) {\n			if (next != 0 && next != 0xffff) {\n				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);\n			} else {\n				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);\n			}\n		}\n'
F1 = '		i = 0;\n		do {\n			if (next != 0 && next != 0xffff) {\n				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);\n			} else {\n				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);\n			}\n			i++;\n		} while (i < blocks);\n'
FS = [('', []), ('fd', [(F0, F1)])]
B0 = '	for (b = 0; b < blocks; b++) {\n		small ='
B1 = '	b = 0;\n	do {\n		small ='
BE0 = '		}\n	}\n#undef BLK\n'
BE1 = '		}\n		b++;\n	} while (b < blocks);\n#undef BLK\n'
BL = [('', []), ('bd', [(B0, B1), (BE0, BE1)])]
D = [('', []), ('nd', [(DEAD, '')])]
AXES = [FS, BL, D]
FLAGS = []
