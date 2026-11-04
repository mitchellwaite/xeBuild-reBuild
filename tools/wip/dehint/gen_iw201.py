# attempt 13: on near8 + no imgWriteHdr + the real bitfield for the block type (build/iw/a13/n8_bf.c, only writeFsTable 4 left):
# t without its pin, partial's test, pages' forms.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/n8_bf.c')
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
TD = '	uint8_t t;\n'
T1 = "		t = type - '1';\n"
T2 = '		if (t < 15) {\n'
PT = '		if (partial > 0) {\n'
PD = '	int partial;\n'
AXES = [
 [('', []),
  ('np', [(PIN, '')]),
  ('nu', [(PIN, ''), (TD, '	unsigned t;\n'), (T2, '		if ((uint8_t)t < 15) {\n')]),
  ('n0', [(PIN, ''), (TD, ''), (T1, ''), (T2, "		if (type >= '1' && type <= '?') {\n")]),
  ('n1', [(PIN, ''), (TD, ''), (T1, ''), (T2, "		if (type > '0' && type < '@') {\n")]),
  ('nI', [(PIN, ''), (TD, '	int t;\n'), (T2, '		if ((uint8_t)t < 15) {\n')]),
  ('nW', [(PIN, ''), (TD, '	uint32_t t;\n'), (T1, "		t = (uint8_t)(type - '1');\n")]),
 ],
 [('', []),
  ('G', [(PT, '		if (partial) {\n')]),
  ('H', [(PT, '		if (partial >= 1) {\n')]),
 ],
 [('', []),
  ('pu', [(PD, '	unsigned partial;\n')]),
  ('pb', [(PD, '	_Bool partial;\n')]),
 ],
]
FLAGS = []
