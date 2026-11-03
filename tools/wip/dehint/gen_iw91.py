# attempt 6: q1: partial's forms x its type x pg's forms
PART = "		partial = len < 0x4000 && type != 0 && type != '0';\n"
PD = '	uint8_t partial;\n'
P = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
PF = [
 "len < 0x4000 && type != '0' && type != 0",
 "len < 0x4000 && (type != 0 && type != '0')",
 "len <= 0x3fff && type != 0 && type != '0'",
 "len < 0x4000 && type && type != '0'",
 "len < 0x4000 && type != 0 && type != 0x30",
 "(len >> 14) == 0 && type != 0 && type != '0'",
 "len / 0x4000 == 0 && type != 0 && type != '0'",
 "!(len >= 0x4000 || type == 0 || type == '0')",
 "!(len >= 0x4000) && !(type == 0 || type == '0')",
 "len < 0x4000 && !(type == 0 || type == '0')",
 "len < 0x4000 && (type != 0) & (type != '0')",
 "(len < 0x4000) & (type != 0) & (type != '0')",
 "(type != 0) & (type != '0') && len < 0x4000",
]
AXES = [
 [('', [])] + [('f%d' % i, [(PART, '		partial = %s;\n' % f)]) for i, f in enumerate(PF)],
 [('', []), ('i', [(PD, '	int partial;\n')]), ('B', [(PD, '	_Bool partial;\n')])],
 [('', []),
  ('pa', [(P, '			s = xb.spare + (pg + p + b * 32) * 16;\n'), (OUT, OUT + '		pg = start * 32;\n')]),
  ('pb', [(P, '			s = xb.spare + (pg + p + b * 32) * 16;\n'), (INNER, '		pg = start * 32;\n' + INNER)]),
  ('pc', [(P, '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n')]),
  ('pe', [(P, '			pg = b * 32 + p;\n			s = xb.spare + (start * 32 + pg) * 16;\n')]),
  ('ph', [(P, '			pg = start * 32 + b * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
 ],
]
BASE = 'build/iw/a6/q1.c'
FLAGS = []
