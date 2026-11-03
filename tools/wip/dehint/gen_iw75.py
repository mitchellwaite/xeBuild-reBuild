# attempt 5: where t is computed against the _Bool partial (m3); the lim hoist order follows the blocks
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m3.c')
T = "		t = type - '1';\n"
NP = '		if (len % 512)\n'
LAB = '''			lnp2: __attribute__((hot));
		}
'''
PIN = '			__asm__("" :: "g"(t));\n'
IF3 = "		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n"
AXES = [
 [('t0', []),
  ('tnp', [(T, ''), (NP, T + NP)]),
  ('tlab', [(T, ''), (LAB, LAB + T)]),
  ('tp', [(T, ''), ('		p = 0;\n		if (t < 15) {\n', '		p = 0;\n' + T + '		if (t < 15) {\n')]),
  ('tin', [(T, ''), ('		if (t < 15) {\n', "		if ((t = type - '1') < 15) {\n")]),
 ],
 [('', []),
  ('i3', [(IF3, "		if (type != 0 && type != '0')\n			if (len < 0x4000)\n				partial = 1;\n")]),
  ('i7', [(IF3, "		if (type != 0 && type != '0') {\n			if (len < 0x4000)\n				partial = 1;\n		}\n")]),
  ('i8', [(IF3, "		if (type == 0 || type == '0')\n			;\n		else if (len < 0x4000)\n			partial = 1;\n")]),
 ],
 [('', []), ('nopin', [(PIN, '')])],
]
FLAGS = []
