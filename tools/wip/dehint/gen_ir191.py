"""detectController: the metadata's BlockID0:4 as bit-fields, pin_lo and pin_found on and off.  checkBlock's volatile as a bit-field."""
FOCUS = ['_detectController', '_checkBlock']
BASE = 'build/ir/a12/bf.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
NL = chr(10)
DEF = '''struct bigMeta { uint8_t badBlock; uint8_t blockId1; uint8_t blockId0 : 4; uint8_t unused0 : 4; };
struct smallMeta { uint8_t blockId1; uint8_t blockId0 : 4; uint8_t unused0 : 4; };

'''
FN = 'int checkBlock(uint8_t *b, int block, int numBlocks)'
assert FN in src
PINF = '''		if (n > 1)
			__asm__("" : "+a"(found));
'''
PINL = '''					__asm__("" : : "a"(lo));
'''
H0 = '''			hi = (b[514] & 0xf) * 256;
			lo = b[513];
'''
T2 = '''				if (lo2 + (b[513] & 0xf) * 256 == i) {
'''
assert PINF in src and PINL in src and H0 in src and T2 in src
BIG = '((struct bigMeta *)(b + 512))'
SMALL = '((struct smallMeta *)(b + 512))'
PF = [('pf', []), ('nf', [(PINF, '')])]
PL = [('pl', []), ('nl', [(PINL, '')])]
HI = [
 ('h0', []),
 ('h1', [(H0, '			hi = %s->blockId0 * 256;\n			lo = b[513];\n' % BIG)]),
 ('h2', [(H0, '			hi = %s->blockId0 << 8;\n			lo = b[513];\n' % BIG)]),
 ('h3', [(H0, '			lo = b[513];\n			hi = %s->blockId0 * 256;\n' % BIG)]),
 ('h4', [(H0, '			hi = %s->blockId0 * 256;\n			lo = %s->blockId1;\n' % (BIG, BIG))]),
]
T = [
 ('t0', []),
 ('t1', [(T2, '				if (lo2 + %s->blockId0 * 256 == i) {\n' % SMALL)]),
 ('t2', [(T2, '				if (lo2 + (%s->blockId0 << 8) == i) {\n' % SMALL)]),
]
AXES = [[('d', [(FN, DEF + FN)])], PF, PL, HI, T]
