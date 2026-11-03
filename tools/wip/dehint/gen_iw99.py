# attempt 6: r1 (no pg, no dead tests: clone lost, evaluation 360, otherwise only writeFsTable 4): pg outside the inner loop, smaller time benefit
import os
S = '			s = xb.spare + (BLK * 32 + p) * 16;\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
PR = '		p = 0;\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
U = ['(pg + p + b * 32)', '(pg + b * 32 + p)', '(b * 32 + pg + p)', '(p + pg + b * 32)', '(p + b * 32 + pg)']
AXES = [
 [('o', [(OUT, OUT + '		pg = start * 32;\n')]),
  ('b', [(INNER, '		pg = start * 32;\n' + INNER)]),
  ('r', [(PR, '		pg = start * 32;\n' + PR)]),
  ('e', [(PART, PART + '		pg = start * 32;\n')]),
  ('bb', [(INNER, '		pg = (start + b) * 32;\n' + INNER)]),
 ],
 [('u%d' % i, [(S, '			s = xb.spare + %s * 16;\n' % u)]) for i, u in enumerate(U)],
 [('', []),
  ('pb', [(PART, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
  ('pa', [(PART, "		partial = len < 0x4000 && type != 0 && type != '0';\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r1.c')
FLAGS = []
