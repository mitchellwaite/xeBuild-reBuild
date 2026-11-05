"""getImageSmc, `ok &&` gone, s4 (bad arm inline, not-sane just before the return block: names right, P 80.9): the allocno order (r88 size before r104 swap result) decides the rest: types of size."""
FOCUS = ['_getImageSmc']
BASE = 'build/ir/a11/s4.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
NL = chr(10)
SZ = '	int size = SWAP32(h->smcBootSize);' + NL
LS = 'static void loadSmc(int addr, int size)' + NL
LP = {'li': [], 'lu': [(LS, 'static void loadSmc(int addr, uint32_t size)' + NL)], 'luu': [(LS, 'static void loadSmc(uint32_t addr, uint32_t size)' + NL)]}
S = {
 'si': [],
 'su': [(SZ, '	uint32_t size = SWAP32(h->smcBootSize);' + NL)],
 'sl': [(SZ, '	long size = SWAP32(h->smcBootSize);' + NL)],
 'sul': [(SZ, '	unsigned long size = SWAP32(h->smcBootSize);' + NL)],
}
B = {
 'b': [],
 'bm': [('	bad = size != 0x3000 && size != 0x3800;' + NL, '	bad = (size & ~0x800) != 0x3000;' + NL)],
}
AXES = [list(S.items()), list(LP.items()), list(B.items())]
