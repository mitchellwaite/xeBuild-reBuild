# attempt 7: gen_iw122 with the optimize attribute removed: one dead test in writeFsTable, any position and body, net -1 if identical
import os
BL = '		blk = start + b;\n'
SM = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"
U1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
DD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
POSN = {
 'p3': None,
 'p2': '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n',
 'p1': '	p = buf;\n',
 'p0': '	buf = malloc(0x4000);\n',
 'p5': '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n',
}
BODY = ['off += 0x4000;', 'off += 0x8000;', 'off += 0x200;', 'off -= 0x4000;', 'off += 2;', 'blk += 2;', 'blk = 0;', 'off = 0;']
A = []
for pn, ps in POSN.items():
    for k, b in enumerate(BODY):
        d = '	if ((off & 0x3fff) > 0x3fff)\n		%s\n' % b
        if ps is None:
            A.append((pn + 'b%d' % k, [(DD, d)]))
        else:
            A.append((pn + 'b%d' % k, [(DD, ''), (ps, d + ps)]))
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
AXES = [
 [('noopt', [(OPT, 'void writeFsTable')])],
 [('', []),
  ('nob', [(BL, ''), (U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n')]),
 ],
 [('', []),
  ('nos', [(SM, "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n")]),
  ('nos2', [(SM, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
 ],
 A,
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a7.c')
FLAGS = []
