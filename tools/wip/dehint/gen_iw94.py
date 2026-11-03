# attempt 6: r0: forms of the off-only statement, the writeFsTable compare wants the name ivopts releases last above end's
import os
P = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
WF = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
F = [
 'pg = start << 5;\n			s = xb.spare + (pg + p + b * 32) * 16;',
 'pg = 32 * start;\n			s = xb.spare + (pg + p + b * 32) * 16;',
 'pg = (off - x) / 512;\n			s = xb.spare + (pg + p + b * 32) * 16;',
 'pg = (off - x) >> 9;\n			s = xb.spare + (pg + p + b * 32) * 16;',
 'pg = start * 32;\n			s = xb.spare + (b * 32 + pg + p) * 16;',
 'pg = start * 32;\n			pg += p + b * 32;\n			s = xb.spare + pg * 16;',
 'pg = start * 32;\n			pg += b * 32 + p;\n			s = xb.spare + pg * 16;',
 'pg = start * 32;\n			pg += b * 32;\n			s = xb.spare + (pg + p) * 16;',
 'pg = start * 512;\n			s = xb.spare + pg + (b * 32 + p) * 16;',
 'pg = start * 512;\n			s = xb.spare + (b * 32 + p) * 16 + pg;',
 'pg = start * 32;\n			s = xb.spare + pg * 16 + (b * 32 + p) * 16;',
 'pg = start * 32;\n			s = xb.spare + (pg + b * 32) * 16 + p * 16;',
 'pg = start * 32;\n			s = xb.spare + (pg * 16) + b * 512 + p * 16;',
 'pg = start * 32;\n			s = &xb.spare[(pg + p + b * 32) * 16];',
 'pg = start * 32;\n			s = (pg + p + b * 32) * 16 + xb.spare;',
 'pg = start * 32 + p;\n			s = xb.spare + (pg + b * 32) * 16;',
 'pg = b * 32 + p;\n			s = xb.spare + (pg + start * 32) * 16;',
 'pg = start * 32;\n			pg = pg + p;\n			s = xb.spare + (pg + b * 32) * 16;',
 'pg = p + b * 32;\n			pg += start * 32;\n			s = xb.spare + pg * 16;',
 'pg = p + start * 32;\n			pg += b * 32;\n			s = xb.spare + pg * 16;',
]
AXES = [
 [('', [])] + [('f%d' % i, [(P, '			%s\n' % f)]) for i, f in enumerate(F)],
 [('', []), ('wi', [(WF, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
