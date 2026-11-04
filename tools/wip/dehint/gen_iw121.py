# attempt 7: finalizeImage without the "a"(xb.hdr) pin: forms of the helpers it inlines (pageErased, calcPageEcc), and how the call is written
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
PE = '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
'''
CE = '''	spare[12] = (spare[12] & 0x3f) + (val << 6);
	spare[13] = val >> 2;
	spare[14] = val >> 10;
	spare[15] = val >> 18;
'''
CEH = '	uint32_t val = calcEcd((uint8_t *)data, spare);\n\n' + CE
TEST = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
'''
AXES = [
 [('nopin', [(PIN, '')])],
 [('', []),
  ('p1', [(PE, '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			break;
	if (i < 512)
		return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
''')]),
  ('p2', [(PE, '''	for (i = 0; i < 512; i++) {
		if (data[i] != 0xff)
			return 0;
	}
	if (spareUsed(spare))
		return 0;
	return 1;
''')]),
  ('p3', [(PE, '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	return !spareUsed(spare);
''')]),
  ('p4', [(PE, '''	const uint8_t *e = data + 512;

	while (data < e)
		if (*data++ != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
''')]),
  ('p5', [(PE, '''	int ok = 1;

	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			ok = 0;
	return ok;
''')]),
 ],
 [('', []),
  ('c1', [(CE, '''	uint8_t b12 = (spare[12] & 0x3f) + (val << 6);

	spare[12] = b12;
	spare[13] = val >> 2;
	spare[14] = val >> 10;
	spare[15] = val >> 18;
''')]),
  ('c2', [(CE, '''	spare[15] = val >> 18;
	spare[14] = val >> 10;
	spare[13] = val >> 2;
	spare[12] = (spare[12] & 0x3f) + (val << 6);
''')]),
  ('c3', [(CE, '''	spare[12] = (spare[12] & 0x3f) | (val << 6);
	spare[13] = val >> 2;
	spare[14] = val >> 10;
	spare[15] = val >> 18;
''')]),
 ],
 [('', []),
  ('t1', [(TEST, '''			{
				uint8_t *d = xb.hdr + (b * 32 + p) * 512, *e = xb.spare + (b * 32 + p) * 16;

				if (!pageErased(d, e))
					calcPageEcc(d, e);
			}
''')]),
  ('t2', [(TEST, '''			if (pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				;
			else
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
''')]),
  ('t3', [('	uint8_t *raw, *s, *spare;\n', '	uint8_t *raw, *s, *spare, *hdr;\n'), (TEST, '''			hdr = xb.hdr + (b * 32 + p) * 512;
			if (!pageErased(hdr, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(hdr, xb.spare + (b * 32 + p) * 16);
''')]),
 ],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a7.c')
FLAGS = []
FOCUS = ['_finalizeImage', '_pageErased', '_calcPageEcc', '_blockEccOk', '_blockPagesErased', '_writeImage']
