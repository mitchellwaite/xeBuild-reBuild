# attempt 2, on drafts/image_write.c: pin_t gone; the slots of t and partial are chosen by LRA's frequency order, so forms of
# the t test and partial's test.  Result: only the two byte slots swap (10 lines).
BASE = 'tools/wip/dehint/drafts/image_write.c'
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
TT = '''		p = 0;
		if (t < 15) {
''' + PIN + '''			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
		}
'''
BODY = '''			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
'''
T = "		t = type - '1';\n"
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
AXES = [
 [('', [(PIN, '')]),
  ('T1', [(TT, '		if (t < 15) {\n' + BODY + '		} else\n			p = 0;\n')]),
  ('T2', [(TT, '		if (t >= 15)\n			p = 0;\n		else {\n' + BODY + '		}\n')]),
  ('T3', [(TT, "		p = 0;\n		if (t <= 14) {\n" + BODY + '		}\n')]),
  ('T4', [(TT, "		p = 0;\n		if (t < 15 && (xb.bigBlock ? off & 0x1ffff : off & 0x3fff))\n			p = (xb.bigBlock ? off & 0x1ffff : off & 0x3fff) / 512;\n")]),
  ('T5', [(T, ''), (TT, "		p = 0;\n		if ((uint8_t)(type - '1') < 15) {\n" + BODY + '		}\n')]),
  ('T6', [(TT, "		p = 0;\n		if (type >= '1' && type < '1' + 15) {\n" + BODY + '		}\n')]),
  ('T7', [(TT, "		p = 0;\n		if (t < 15 && t != 0xff) {\n" + BODY + '		}\n')]),
 ],
 [('', []),
  ('L1', [(LNP, '		if (partial) {\n			lnp2: __attribute__((hot));\n		} else\n			npages = 32;\n')]),
 ],
 [('', []),
  ('P1', [(P, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
  ('P2', [(P, "		partial = type != '0' && type != 0 && len < 0x4000;\n")]),
  ('P3', [(P, "		partial = (type != 0 && type != '0') ? len < 0x4000 : 0;\n")]),
  ('P4', [(P, "		partial = type && type != '0' && len < 0x4000;\n")]),
  ('P5', [(P, "		partial = 0;\n		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n")]),
 ],
]
