# attempt 17: neighbours of build/iw/a17/n12.c (if/else calls, no dead test, no optimize, `left = left - pages`): 12 lines, 3 tricks if it lands. Cross of what moved names in gen_iw234-236.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/n12.c')
D = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n	int left;\n'
BLK0 = '			blk = start + b;\n			memset(s, 0, 16);\n'
SM = '		small = type != 0 && type != \'0\';\n		partial = small && len < 0x4000;\n'
BG = '						pages = len / 512;\n						if (len % 512)\n							pages++;\n'
SA = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
AXES = [
 [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
 [('', []), ('bk', [(BLK0, '			memset(s, 0, 16);\n'), ('	for (b = 0; b < blocks; b++) {\n		small =', '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n		small =')])],
 [('', []),
  ('lu', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, left;\n')]),
  ('pi', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages;\n	int left, pages;\n')])],
 [('', []), ('bq', [(BG, '						pages = len % 512 ? len / 512 + 1 : len / 512;\n')])],
 [('', []), ('si', [(SA, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n')])],
 [('', []), ('am', [(SM, '		partial = (len < 0x4000) & (type != 0) & (type != \'0\');\n')])],
 [('', []), ('fm', [('left = left - pages;\n						s[9] = left >> 2;', 's[9] = (int)(left - pages) >> 2;')]), ('fp', [('left = left - pages;\n						s[9] = left >> 2;', 'left -= pages;\n						s[9] = left >> 2;')])],
]
FLAGS = []
