# attempt 11: on near11 (g3).  Another source of P(partial) >= 55%: PRED_OPCODE_NONEQUAL (72%) fires on `x != C` with C nonzero, if the front end can't fold it (x not a truth value).  So partial as a page-count kind.  With and without the pin on t (t's tie needs 50%).
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g3.c')
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
IF = '		if (partial) {\n'
TD = '	unsigned t;\n'
C = '		if ((uint8_t)t < 15) {\n'
NP = '''		if (partial) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
ARM = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
CD = "len < 0x4000 && type != 0 && type != '0'"
CA = "(len < 0x4000) & (type != 0) & (type != '0')"
AXES = [
 [('K1', [(PA, '		partial = 1;\n		if (%s)\n			partial = 2;\n' % CD), (NP, NP.replace('if (partial)', 'if (partial != 1)'))]),
  ('K2', [(PA, '		partial = 1 + (%s);\n' % CA), (NP, NP.replace('if (partial)', 'if (partial != 1)'))]),
  ('K3', [(PA, '		partial = 1;\n		if (%s)\n			partial = 2;\n' % CD), (NP, '		if (partial == 1)\n			npages = 32;\n		else {\n' + ARM + '		}\n')]),
  ('K4', [(PA, '		partial = 1 + (%s);\n' % CA), (NP, '		if (partial == 1)\n			npages = 32;\n		else {\n' + ARM + '		}\n')]),
  ('K5', [(PA, '		partial = 32;\n		if (%s)\n			partial = 0;\n' % CD), (NP, NP.replace('if (partial)', 'if (partial != 32)'))]),
  ('K6', [(PA, '		partial = 32;\n		if (%s)\n			partial = 0;\n' % CD), (NP, '		if (partial == 32)\n			npages = 32;\n		else {\n' + ARM + '		}\n')]),
  ('K7', [(PA, '		partial = (%s) ? 2 : 1;\n' % CA), (NP, NP.replace('if (partial)', 'if (partial != 1)'))]),
 ],
 [('', []), ('t8', [(TD, '	uint8_t t;\n'), (C, '		if (t < 15) {\n')]),
  ('t8p', [(TD, '	uint8_t t;\n'), (C, '		if (t < 15) {\n			__asm__("" :: "g"(t));\n')]),
 ],
]
FLAGS = []
