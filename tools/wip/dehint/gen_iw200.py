# attempt 13: near11 without imgWriteHdr (build/iw/a13/n_nohdr.c). Natural spellings of imgAdd's stand-ins, as the Linux
# build's imgAdd reads: start = off >> 14, ((start + b) * 32 + p) * 16, tail && pad == 1, range test on type. Each off/on.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/n_nohdr.c')
ST = '	start = (off - x) >> 14;\n'
PG = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
PAD = '	if (pad == 1) if (tail)\n'
T1 = "		t = type - '1';\n"
T2 = '		if ((uint8_t)t < 15) {\n'
BL = '		blk = start + b;\n'
BS = '				((struct spb *)s)->b2lo = blk >> 8;\n'
AXES = [
 [('', []), ('st', [(ST, '	start = off >> 14;\n')])],
 [('', []),
  ('pg1', [(PG, '			s = xb.spare + ((start + b) * 32 + p) * 16;\n')]),
  ('pg2', [(PG, '			s = xb.spare + (start * 32 + b * 32 + p) * 16;\n')]),
  ('pg3', [(PG, '			s = xb.spare + (blk * 32 + p) * 16;\n')]),
  ('pg4', [(PG, '			pg = blk * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
  ('pg5', [(PG, '			pg = (start + b) * 32 + p;\n			s = xb.spare + pg * 16;\n')]),
 ],
 [('', []),
  ('pa', [(PAD, '	if (pad == 1 && tail)\n')]),
  ('pb', [(PAD, '	if (tail && pad == 1)\n')]),
 ],
 [('', []),
  ('t8', [('	unsigned t;\n', '	uint8_t t;\n'), (T2, '		if (t < 15) {\n')]),
  ('t0', [('	unsigned t;\n', ''), (T1, ''), (T2, "		if (type >= '1' && type <= '?') {\n")]),
  ('t1', [('	unsigned t;\n', ''), (T1, ''), (T2, "		if (type > '0' && type < '@') {\n")]),
  ('t2', [('	unsigned t;\n', ''), (T1, ''), (T2, "		if ((uint8_t)(type - '1') < 15) {\n")]),
 ],
 [('', []), ('bl', [(BL, ''), (BS, '				((struct spb *)s)->b2lo = (start + b) >> 8;\n'), ('	uint32_t b, blk;\n', '	uint32_t b;\n')])],
]
FLAGS = []
