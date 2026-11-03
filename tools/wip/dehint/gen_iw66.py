# attempt 4: imgAdd without a5 and/or a2: a natural source of ipa-cp time benefit on off in the loops: computing from off inside the loops (LIM hoists it again)
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a4.c')
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
START = '	start = (off - x) >> 14;\n'
LOOPB = '	for (b = 0; b < blocks; b++) {\n'
LOOPI = '		for (i = 0; i < blocks; i++) {\n'
P = '''			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
'''
AXES = [
 [('', []), ('xA2', [(A2, '')])],
 [('', []), ('xA5', [(A5, '')])],
 [('', []),
  ('sB', [(START, ''), (LOOPB, LOOPB + '		start = (off - (off & 0x3fff)) >> 14;\n')]),
  ('sB2', [(LOOPB, LOOPB + '		start = (off - x) >> 14;\n')]),
  ('sB3', [(LOOPB, LOOPB + '		start = (off - (off & 0x3fff)) >> 14;\n')]),
  ('sI', [(LOOPI, LOOPI + '			start = (off - (off & 0x3fff)) >> 14;\n')]),
  ('sBI', [(LOOPB, LOOPB + '		start = (off - (off & 0x3fff)) >> 14;\n'), (LOOPI, LOOPI + '			start = (off - (off & 0x3fff)) >> 14;\n')]),
  ('xB', [(LOOPB, LOOPB + '		x = off & 0x3fff;\n')]),
  ('xI', [(LOOPI, LOOPI + '			x = off & 0x3fff;\n')]),
  ('xBI', [(LOOPB, LOOPB + '		x = off & 0x3fff;\n'), (LOOPI, LOOPI + '			x = off & 0x3fff;\n')]),
  ('xBs', [(LOOPB, LOOPB + '		x = off & 0x3fff;\n		start = (off - x) >> 14;\n')]),
  ('xIs', [(LOOPI, LOOPI + '			x = off & 0x3fff;\n			start = (off - x) >> 14;\n')]),
  ('xBIs', [(LOOPB, LOOPB + '		x = off & 0x3fff;\n		start = (off - x) >> 14;\n'), (LOOPI, LOOPI + '			x = off & 0x3fff;\n			start = (off - x) >> 14;\n')]),
 ],
]
