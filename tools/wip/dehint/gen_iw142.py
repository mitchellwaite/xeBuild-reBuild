# attempt 8: t's type (an extra conversion statement moves the free list in the clones) x pages' spelling and place per arm, from n7, pin kept.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n7.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
D = '	uint8_t t;\n'
C = 'if (t < 15) {'
TY = [
 ('', []),
 ('ch', [(D, '	char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('ui', [(D, '	unsigned t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('sc', [(D, '	signed char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
]
B0 = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n'
S0 = '			} else {\n				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct sps *)s)->b1lo = BLK >> 8;\n'
ST1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n'
BIGTOP = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
BT1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n'
SPELL = {
 't': ['pages = len % 512 ? len / 512 + 1 : len / 512;'],
 'i': ['pages = len / 512;', 'if (len % 512)', '\tpages++;'],
 'e': ['if (len % 512)', '\tpages = len / 512 + 1;', 'else', '\tpages = len / 512;'],
}


def ind(k, n):
    return ''.join('\t' * n + l + '\n' for l in SPELL[k])


POS = []
for b in 'tie':
    for s in 'te':
        POS.append(('Bin%s+Stop%s' % (b, s), [(B0, ind(b, 6) + '						left = pages;\n'), (S0, '			} else {\n' + ind(s, 4) + '				((struct sps *)s)->b1lo = BLK >> 8;\n')]))
        POS.append(('Btop%s+St1%s' % (b, s), [(B0, '						left = pages;\n'), (S0, '			} else {\n				((struct sps *)s)->b1lo = BLK >> 8;\n'),
                                              (BIGTOP, '			if (xb.bigBlock) {\n' + ind(b, 4) + '				((struct spb *)s)->b2lo'),
                                              (ST1, '				if (type > 1) {\n' + ind(s, 5) + ST1.split('\n', 1)[1])]))
        POS.append(('Bt1%s+Stop%s' % (b, s), [(B0, '						left = pages;\n'), (S0, '			} else {\n' + ind(s, 4) + '				((struct sps *)s)->b1lo = BLK >> 8;\n'),
                                              (BT1, '				if (type > 1) {\n' + ind(b, 5) + BT1.split('\n', 1)[1])]))
AXES = [TY, POS]
