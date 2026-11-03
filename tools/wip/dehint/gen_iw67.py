# attempt 4: imgAdd without a5/a2: the loops' block number spelled from off itself (natural ipa-cp time benefit on off), start kept or not
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a4.c')
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
START = '	start = (off - x) >> 14;\n'
BLK = '#define BLK (start + b)\n'
NX = '''				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
'''
LAST = '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n'
S1 = '(off >> 14)'
S2 = '((off - x) >> 14)'
S3 = '((off - (off & 0x3fff)) >> 14)'
AXES = [
 [('', []), ('xA5', [(A5, '')])],
 [('', []), ('xA2', [(A2, '')])],
 [('', []), ('s0', [(START, '	start = off >> 14;\n')])],
 [('', []), ('b1', [(BLK, f'#define BLK ({S1} + b)\n')]), ('b2', [(BLK, f'#define BLK ({S2} + b)\n')]), ('b3', [(BLK, f'#define BLK ({S3} + b)\n')])],
 [('', []), ('n1', [(NX, NX.replace('start', S1))]), ('n2', [(NX, NX.replace('start', S2))]), ('n3', [(NX, NX.replace('start', S3))])],
 [('', []), ('l1', [(LAST, LAST.replace('start', S1))])],
]
