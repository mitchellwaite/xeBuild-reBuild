# attempt 2, on drafts/image_write.c: pin_t gone.  t and partial tie on frequency (900 each) so LRA's slot order falls to regno,
# i.e. SSA version at expand (partial _279 < t _280): t's definition earlier, to give it the lower version.
BASE = 'tools/wip/dehint/drafts/image_write.c'
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
T = "		t = type - '1';\n"
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
HEAD = "	x = off & 0x3fff;\n"
LOOP = "	for (b = 0; b < blocks; b++) {\n"
MC = "	memcpy(xb.hdr + off, src, len);\n"
AXES = [
 [('', [(PIN, '')])],
 [('', []),
  ('t0', [(T, ''), (HEAD, "	t = type - '1';\n" + HEAD)]),
  ('t1', [(T, ''), (LOOP, "	t = type - '1';\n" + LOOP)]),
  ('t2', [(T, ''), (MC, "	t = type - '1';\n" + MC)]),
  ('t3', [(T, ''), ('	uint8_t t;\n', "	uint8_t t = type - '1';\n")]),
  ('t4', [(T, ''), ("	uint32_t x, first", "	uint8_t t2 = type - '1';\n	uint32_t x, first"), ('	uint8_t t;\n', ''), ('t < 15', 't2 < 15')]),
 ],
 [('', []),
  ('p1', [(P, ''), (LOOP, P[1:] + LOOP)]),
  ('p2', [(P, ''), (MC, P[1:] + MC)]),
 ],
]
