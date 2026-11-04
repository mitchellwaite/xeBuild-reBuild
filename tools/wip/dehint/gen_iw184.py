# attempt 11: on build/iw/a11/g0.c (gen_iw183 P1+G: no hot label, `if (partial)`, pages at src's place).  t's type, with and without the pin, under the inline probe flag.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g0.c')
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
D = '	uint8_t t;\n'
T = "		t = type - '1';\n"
C = '		if (t < 15) {\n'
AXES = [
 [('', []), ('nopin', [(PIN, '')])],
 [('', []),
  ('ui', [(D, '	unsigned t;\n'), (C, '		if ((uint8_t)t < 15) {\n')]),
  ('ch', [(D, '	char t;\n'), (C, '		if ((uint8_t)t < 15) {\n')]),
  ('in', [(D, '	int t;\n'), (C, '		if ((uint8_t)t < 15) {\n')]),
  ('u2', [(D, '	unsigned t;\n'), (T, "		t = (uint8_t)(type - '1');\n")]),
 ],
 [('', []),
  ('aft', [(T, ''), ('		p = 0;\n		if (', "		p = 0;\n		t = type - '1';\n		if (")]),
  ('fst', [(T, ''), ("		partial = (len < 0x4000)", "		t = type - '1';\n		partial = (len < 0x4000)")]),
 ],
]
FLAGS = ['--param', 'inline-min-speedup=11']
