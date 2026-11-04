# attempt 16: `left` and s[9] forms (gen_iw214's c1-c7 plus more) x the two pages spellings (only those with a low line count in gen_iw228) on a15_dead. c4 on the dead draft fixes C1 (gen_iw214 c4).
import os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('g8', os.path.join(here, 'gen_iw228.py')); g8 = importlib.util.module_from_spec(sp); sp.loader.exec_module(g8)
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15_dead.c')
OLD = '''						left = pages;
						if (left & 3)
							left = (left + 4) & ~3;
						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;
'''
I = '\t' * 6
def f(s):
    return ''.join(I + l + '\n' for l in s.split('\n'))
C = {'c0': None,
 'c1': 'left = pages;\nif (left & 3)\n	left = (left + 4) & ~3;\nleft = ((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left;\ns[9] = left >> 2;',
 'c2': 'if (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - pages) >> 2;',
 'c3': 'left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\nif (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (left - pages) >> 2;',
 'c4': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\nif (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (left - pages) >> 2;',
 'c8': 'left = 256;\nif (off & 0x1ffff)\n	left -= (off & 0x1ffff) / 512;\nif (pages & 3)\n	pages = (pages + 4) & ~3;\ns[9] = (left - pages) >> 2;',
 'c9': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\nif (pages & 3)\n	pages = (pages + 4) & ~3;\nleft -= pages;\ns[9] = left >> 2;',
 'c10': 'if (pages & 3)\n	pages = (pages + 4) & ~3;\nif (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\ns[9] = (left - pages) >> 2;',
 'c11': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\nif (pages & 3) {\n	pages += 4;\n	pages &= ~3;\n}\ns[9] = (left - pages) >> 2;',
 'c12': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\nleft -= pages & 3 ? (pages + 4) & ~3 : pages;\ns[9] = left >> 2;',
 'c13': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\ns[9] = (left - (pages & 3 ? (pages + 4) & ~3 : pages)) >> 2;',
 'c14': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\npages = pages & 3 ? (pages + 4) & ~3 : pages;\ns[9] = (left - pages) >> 2;',
 'c15': 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\nif (pages & 3)\n	s[9] = (left - ((pages + 4) & ~3)) >> 2;\nelse\n	s[9] = (left - pages) >> 2;',
}
CA = [(k, [(OLD, f(v))] if v else []) for k, v in C.items()]
AB = [a for a in g8.AB if a[0] in ('ba', 'bt', 'bm', 'bi')]
AS = [a for a in g8.AS if a[0] in ('st', 'sa', 'sm', 'si')]
TL = [('', []), ('to', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')])]
AXES = [CA, AB, AS, TL]
FLAGS = []
