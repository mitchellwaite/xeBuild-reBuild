# attempt 6: around p0 (build/iw/a6/p0.c: a2, a5 gone, `pg = start * 32` in the inner loop)
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
LP = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
P = '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
PART = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
T = "		t = type - '1';\n"
WF = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
AXES = [
 [('', []), ('noc4', [(C4, '')])],
 [('', []), ('nolp', [(LP, '')])],
 [('', []),
  ('pa', [(P, '			s = xb.spare + (pg + b * 32 + p) * 16;\n'), (OUT, OUT + '		pg = start * 32;\n')]),
  ('pb', [(P, '			s = xb.spare + (pg + b * 32 + p) * 16;\n'), (INNER, '		pg = start * 32;\n' + INNER)]),
  ('pc', [(P, '			pg = start * 32;\n			s = xb.spare + (b * 32 + pg + p) * 16;\n')]),
  ('pd', [(P, '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n')]),
  ('pe', [(P, '			pg = b * 32 + p;\n			s = xb.spare + (start * 32 + pg) * 16;\n')]),
  ('pf', [(P, '			pg = start * 512;\n			s = xb.spare + pg + (b * 32 + p) * 16;\n')]),
  ('pg', [(P, '			pg = start * 32;\n			pg += b * 32 + p;\n			s = xb.spare + pg * 16;\n')]),
  ('ph', [(P, '			pg = start * 32 + b * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
 ],
 [('', []), ('t2', [(T + '		if (len % 512)', '		if (len % 512)'), ('		p = 0;\n', T + '		p = 0;\n')]),
  ('t3', [(PART + T, T + PART)])],
 [('', []),
  ('wi', [(WF, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
BASE = 'build/iw/a6/p0.c'
FLAGS = []
