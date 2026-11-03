# attempt 6: a2/a5 replaced by an off-only computation that really is in the spare loop: `start * 32`
# (inline summary: a stmt whose operands all derive from params is time saved when they're known)
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
S = '			s = xb.spare + (BLK * 32 + p) * 16;\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
AXES = [
 [('a2', [(A2, '')]), ('', [])],
 [('a5', [(A5, '')]), ('', [])],
 [('c4', [(C4, '')]), ('', [])],
 [('s1', [(S, '			s = xb.spare + (start * 32 + b * 32 + p) * 16;\n')]),
  ('s2', [(S, '			s = xb.spare + (b * 32 + start * 32 + p) * 16;\n')]),
  ('s3', [(S, '			s = xb.spare + (start * 32 + p + b * 32) * 16;\n')]),
  ('s4', [(S, '			s = xb.spare + start * 512 + b * 512 + p * 16;\n')]),
  ('s5', [(S, '			s = xb.spare + (b * 32 + p + start * 32) * 16;\n')]),
  ('s6', [(S, '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n')]),
  ('s7', [(S, '			s = xb.spare + (start * 32) * 16 + (b * 32 + p) * 16;\n')]),
  ('s8', [(S, '			s = xb.spare + ((b * 32 + p) + (start << 5)) * 16;\n')]),
 ],
]
BASE = 'src/image_write.c'
FLAGS = []
