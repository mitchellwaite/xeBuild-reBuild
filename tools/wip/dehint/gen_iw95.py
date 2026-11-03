# attempt 6: from src: every combination of this attempt's forms and the dead tests, looking for any identical reduction
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
LP = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
S = '			s = xb.spare + (BLK * 32 + p) * 16;\n'
PART = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
FE = '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n'
WF = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
AXES = [
 [('', []), ('a2', [(A2, '')])],
 [('', []), ('c4', [(C4, '')])],
 [('', []), ('a5', [(A5, '')])],
 [('', []), ('lp', [(LP, '')])],
 [('', []), ('pg', [(S, '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n')])],
 [('', []),
  ('f11', [(PART, "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n")]),
  ('f4', [(PART, "		partial = len < 0x4000 && type != 0 && type != '0';\n")])],
 [('', []), ('fe', [(FE, '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
 [('', []), ('wi', [(WF, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
BASE = 'src/image_write.c'
FLAGS = []
