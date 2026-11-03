# attempt 6: family s1: no dead tests, BLK * 32 kept, `pg = off & 0x1ffff;` before `pages` in the inner loop: fsend, partial, tail, t order
import os
FE = '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
TAIL = '		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n'
WF = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
PS = [
 "type != 0 && type != '0' && len < 0x4000",
 "len < 0x4000 && type != 0 && type != '0'",
 "len < 0x4000 && type != '0' && type != 0",
 "(type != 0) & (type != '0') & (len < 0x4000)",
 "(type != 0) & (type != '0') && len < 0x4000",
 "(type != 0 && type != '0') & (len < 0x4000)",
]
AXES = [
 [('', []),
  ('fo', [(FE, '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n')]),
  ('f2', [(FE, '			fsTable[blocks + start - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
 [('', [])] + [('p%d' % i, [(PART, '		partial = %s;\n' % p)]) for i, p in enumerate(PS)],
 [('', []),
  ('t0', [(TAIL, '		if (rem < 0x4000)\n			tail = rem;\n		else\n			tail = rem % 0x4000;\n')])],
 [('', []), ('wi', [(WF, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
 [('', []), ('u8', [('	int partial;\n', '	uint8_t partial;\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/s1.c')
FLAGS = []
