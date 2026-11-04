# attempt 16: on c4 + blk in the page loop (writeFsTable clean, imgAdd one compare): c4's `pages` has no int casts, so imgAdd's PRE has 5 fewer names and its outer compare's bound is a different one. Types and cast forms of pages and left.
import os
BASE = os.environ.get('IWB', 'build/iw/a16/c4g.c')
D = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n	int left;\n'
TY = [('', []),
      ('lu', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, left;\n')]),
      ('pi', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages;\n	int left, pages;\n')]),
      ]
OLD = '''						if (pages & 3)
							pages = (pages + 4) & ~3;
						s[9] = (left - pages) >> 2;
'''
I = '\t' * 6
def f(s):
    return ''.join(I + l + '\n' for l in s.split('\n'))
F = [('', []),
     ('f1', [(OLD, f('if (pages & 3)\n	pages = (pages + 4) & ~3;\nleft -= pages;\ns[9] = left >> 2;'))]),
     ('f2', [(OLD, f('if (pages & 3)\n	pages = (pages + 4) & ~3;\nleft = left - pages;\ns[9] = (uint32_t)left >> 2;'))]),
     ('f3', [(OLD, f('if ((int)pages & 3)\n	pages = ((int)pages + 4) & ~3;\ns[9] = (left - pages) >> 2;'))]),
     ('f4', [(OLD, f('if (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (left - (int)pages) >> 2;'))]),
     ('f5', [(OLD, f('if (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (uint32_t)(left - (int)pages) >> 2;'))]),
     ('f6', [(OLD, f('if (pages & 3) {\n	pages += 4;\n	pages &= ~3;\n}\ns[9] = (left - pages) >> 2;'))]),
     ('f7', [(OLD, f('if ((pages & 3) != 0)\n	pages = (pages + 3) / 4 * 4;\ns[9] = (left - pages) >> 2;'))]),
     ('f8', [(OLD, f('if (pages & 3)\n	pages = (pages & ~3) + 4;\ns[9] = (left - pages) >> 2;'))]),
     ('f9', [(OLD, f('if (pages % 4)\n	pages = (pages + 4) & ~3;\ns[9] = (left - pages) >> 2;'))]),
     ('f10', [(OLD, f('if (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (left - pages) / 4;'))]),
     ]
AXES = [TY, F]
FLAGS = []
