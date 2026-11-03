# attempt 6: r2: `small` temporary x block-number local x fsend, tuples show who gets writeFsTable right
import os
OUT = '	for (b = 0; b < blocks; b++) {\n'
U1 = '				((struct spb *)s)->b2lo = BLK >> 8;\n'
U2 = '				s[1] = BLK;\n'
U4 = '				s[0] = BLK;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
FE = '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
M = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n				((struct spb'
D = '	int partial;\n'
F = {
 'a': "small = (type != 0) & (type != '0');\n		partial = small && len < 0x4000;\n",
 'b': "small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n",
 'c': "small = type != 0 && type != '0';\n		partial = small & (len < 0x4000);\n",
 'e': "small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n",
 'i': "small = type != 0 && type != '0';\n		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n",
}
AXES = [
 [(k, [(PART, '		' + v), (D, D + '	_Bool small;\n')]) for k, v in F.items()],
 [('u1', [(U1, U1.replace('BLK', 'blk'))]),
  ('u24', [(U2, U2.replace('BLK', 'blk')), (U4, U4.replace('BLK', 'blk'))]),
  ('no', [('	uint32_t b, blk;\n', '	uint32_t b;\n')])],
 [('lo', [(OUT, OUT + '		blk = start + b;\n')]),
  ('lm', [(M, '			memset(s, 0, 16);\n			blk = start + b;\n			if (xb.bigBlock) {\n				((struct spb')]),
 ],
 [('', []), ('fo', [(FE, '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
]
AXES[1][2] = ('no', [])
BASE = os.environ.get('IWB', 'build/iw/a6/r2.c')
FLAGS = []
