# attempt 9: on src: the dead test or the optimize attribute gone x named values in imgAdd that die at dce2 in the type-0 and type-0x2c/0x30 copies
# (they move writeFsTable's free list without new CFG).  Wanted: IDENTICAL.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'src/image_write.c')
FOCUS = None
USE = '						s[8] = len >> 8;\n						s[7] = len;\n'
FOR_B = '	for (b = 0; b < blocks; b++) {\n'
FOR_P = '		for (end = p + npages; p < end; p++) {\n'
INNER = '			s = xb.spare + (pg + p + b * 32) * 16;\n'
DECL = '	uint32_t b, blk;\n'
PAGES = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
pl = {'bT': (FOR_B, FOR_B + '		@'), 'pP': (FOR_P, '		@' + FOR_P), 'iT': (FOR_P, FOR_P + '			@'), 'iM': (INNER, INNER + '			@'), 'iP': (PAGES, PAGES + '			@')}
lev = [('', [])]
for k, (a, b) in pl.items():
    lev.append(('hi' + k, [(DECL, DECL + '	uint32_t hi;\n'), (a, b.replace('@', 'hi = len >> 8;\n')), (USE, USE.replace('len >> 8', 'hi'))]))
    lev.append(('h8' + k, [(DECL, DECL + '	uint8_t hi;\n'), (a, b.replace('@', 'hi = len >> 8;\n')), (USE, USE.replace('len >> 8', 'hi'))]))
    lev.append(('lo' + k, [(DECL, DECL + '	uint8_t lo;\n'), (a, b.replace('@', 'lo = len;\n')), ('						s[7] = len;\n', '						s[7] = lo;\n')]))
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
AXES = [lev, [('d', [(DEAD, '')]), ('o', [(OPT, 'void writeFsTable')]), ('do', [(DEAD, ''), (OPT, 'void writeFsTable')])]]
