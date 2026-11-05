"""checkBlock: the volatile re-read of b[513] as a bit-field read (BlockID0:4 of the small block's metadata)."""
FOCUS = ['_checkBlock']
BASE = 'build/ir/a12/bf.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
FN = 'int checkBlock(uint8_t *b, int block, int numBlocks)'
DEF = '''struct bigMeta { uint8_t badBlock; uint8_t blockId1; uint8_t blockId0 : 4; uint8_t unused0 : 4; };
struct smallMeta { uint8_t blockId1; uint8_t blockId0 : 4; uint8_t unused0 : 4; };

'''
V = '''			lba0 = b[512] + (((volatile uint8_t *)b)[513] & 0xf) * 256;
'''
L1 = '''			lba1 = b[513] + (b[514] & 0xf) * 256;
'''
BIG = '((struct bigMeta *)(b + 512))'
SMALL = '((struct smallMeta *)(b + 512))'
A = [
 ('v', []),
 ('s1', [(V, '			lba0 = b[512] + %s->blockId0 * 256;\n' % SMALL)]),
 ('s2', [(V, '			lba0 = %s->blockId1 + %s->blockId0 * 256;\n' % (SMALL, SMALL))]),
 ('s3', [(V, '			lba0 = %s->blockId1 + (%s->blockId0 << 8);\n' % (SMALL, SMALL))]),
]
B = [
 ('l', []),
 ('b1', [(L1, '			lba1 = b[513] + %s->blockId0 * 256;\n' % BIG)]),
 ('b2', [(L1, '			lba1 = %s->blockId1 + %s->blockId0 * 256;\n' % (BIG, BIG))]),
]
AXES = [[('d', [(FN, DEF + FN)])], A, B]
