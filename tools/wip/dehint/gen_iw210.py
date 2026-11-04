# attempt 13: typed views of the spare bytes as real code would have them: a local struct pointer per arm or for the loop, on near13 (w2). Fields for every store, or only the bit stores.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
B0 = '''				((struct spb *)s)->b2lo = blk >> 8;
				((struct spb *)s)->b0 = 0xff;
				s[1] = BLK;
'''
S0 = '''				((struct sps *)s)->b1lo = BLK >> 8;
				((struct sps *)s)->b5 = 0xff;
				s[0] = BLK;
'''
TY = '((struct spt *)s)->type = type;'
AXES = [
 [('', []),
  ('bl', [(B0, '				struct spb *sb = (struct spb *)s;\n\n				sb->b2lo = blk >> 8;\n				sb->b0 = 0xff;\n				sb->b1 = BLK;\n')]),
  ('bm', [(B0, '				struct spb *sb = (struct spb *)s;\n\n				sb->b2lo = blk >> 8;\n				sb->b0 = 0xff;\n				s[1] = BLK;\n')]),
 ],
 [('', []),
  ('sl', [(S0, '				struct sps *ss = (struct sps *)s;\n\n				ss->b1lo = BLK >> 8;\n				ss->b5 = 0xff;\n				ss->b0 = BLK;\n')]),
  ('sm', [(S0, '				struct sps *ss = (struct sps *)s;\n\n				ss->b1lo = BLK >> 8;\n				ss->b5 = 0xff;\n				s[0] = BLK;\n')]),
 ],
 [('', []),
  ('tl', [('				if (type > 1) {\n					' + TY + '\n					if (type != 0x2a', '				if (type > 1) {\n					struct spt *st = (struct spt *)s;\n\n					st->type = type;\n					if (type != 0x2a')]),
 ],
 [('', []),
  ('ts', [('				if (type > 1) {\n					' + TY + '\n					s[9] = 32', '				if (type > 1) {\n					struct spt *st = (struct spt *)s;\n\n					st->type = type;\n					s[9] = 32')]),
 ],
]
FLAGS = []
