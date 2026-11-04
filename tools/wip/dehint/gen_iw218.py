# attempt 14: rejudge found writeFsTable clean with `pg = off & 0x1ffff` as a value in the page loop plus `partial = a && b && c` (gen_iw100 m+pb, imgAdd 100, imgAddFile 22).
# The value's place x partial's form x the `(off & 0x1ffff) ? ...` use. A real local for the block offset (Linux keeps it in one register).
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
P = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
PGS = '			pg = start * 32;\n'
MS = '			memset(s, 0, 16);\n'
IB = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
TT = '				if (type > 1) {\n					((struct spt *)s)->type = type;\n					if (type != 0x2a'
ARM = '					if (type != 0x2a && type != 0x2c) {\n						pages = len / 512;\n'
USE = 's[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;'
NEW = 's[9] = ((V ? 256 - V / 512 : 256) - left) >> 2;'
FOR = '		for (end = p + npages; p < end; p++) {\n'
BL = '		blk = start + b;\n'
HD = '	x = off & 0x3fff;\n'
def pl(lab, a, b, v):
    return (lab, [(a, b), (USE, NEW.replace('V', v))])
PLACES = [('', []),
 pl('ms', MS, MS + '			pg = off & 0x1ffff;\n', 'pg'),
 pl('pre', PGS, '			pg = off & 0x1ffff;\n			pg = start * 32;\n', 'pg') if 0 else ('use', [(USE, '{ uint32_t bo = off & 0x1ffff; s[9] = ((bo ? 256 - bo / 512 : 256) - left) >> 2; }')]),
 ('arm', [(ARM, ARM.replace('						pages = len / 512;\n', '						pg = off & 0x1ffff;\n						pages = len / 512;\n')), (USE, NEW.replace('V', 'pg'))]),
 ('arm2', [(ARM, ARM.replace('						pages = len / 512;\n', '						pages = len / 512;\n')), (USE, 'pg = off & 0x1ffff;\n						s[9] = ((pg ? 256 - pg / 512 : 256) - left) >> 2;')]),
 ('for', [(FOR, FOR + '			uint32_t bo = off & 0x1ffff;\n\n'), (USE, NEW.replace('V', 'bo'))]),
 ('blk', [(BL, BL + '		pg = off & 0x1ffff;\n'), (PGS, '			uint32_t pp = start * 32;\n'), ('(pg + p + b * 32) * 16', '(pp + p + b * 32) * 16'), (USE, NEW.replace('V', 'pg'))]),
 ('hd', [(HD, HD + '	pg = off & 0x1ffff;\n'), (PGS, '			uint32_t pp = start * 32;\n'), ('(pg + p + b * 32) * 16', '(pp + p + b * 32) * 16'), (USE, NEW.replace('V', 'pg'))]),
]
AXES = [
 PLACES,
 [('', []),
  ('aa', [(P, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
  ('a2', [(P, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
  ('a3', [(P, "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n")]),
  ('a4', [(P, "		partial = (type != 0 && type != '0') & (len < 0x4000);\n")]),
 ],
]
FLAGS = []
