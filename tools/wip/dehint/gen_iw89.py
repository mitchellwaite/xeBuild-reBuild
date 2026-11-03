# attempt 6: q0 (all four dead tests gone, pg local) + fsend + partial's type + what else moved a line in the probes
FE = '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n'
PD = '	int partial;\n'
WB = '	buf = malloc(0x4000);\n	p = buf;\n'
TAIL = '''		if (rem < 0x4000)
			tail = rem;
		else
			tail = rem % 0x4000;
'''
PART = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
AXES = [
 [('fe', [(FE, '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
 [('', []), ('u8', [(PD, '	uint8_t partial;\n')]), ('u32', [(PD, '	uint32_t partial;\n')]), ('B', [(PD, '	_Bool partial;\n')])],
 [('', []), ('wb', [(WB, '	p = buf = malloc(0x4000);\n')])],
 [('', []),
  ('t3', [(TAIL, '		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n')]),
  ('t1', [(TAIL, '		tail = rem < 0x4000 ? rem : rem % 0x4000;\n')])],
 [('', []),
  ('p1', [(PART, "		partial = 0;\n		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n")]),
  ('p2', [(PART, "		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n")]),
  ('p3', [(PART, "		partial = (type != 0 && type != '0') && len < 0x4000;\n")]),
  ('p4', [(PART, "		partial = len < 0x4000 && type != 0 && type != '0';\n")])],
]
BASE = 'build/iw/a6/q0.c'
FLAGS = []
