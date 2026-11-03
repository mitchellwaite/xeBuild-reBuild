# attempt 2, on drafts/image_write.c: add2 and/or opt removed, near's shapes, with the merged test's forms as new knobs
BASE = 'tools/wip/dehint/drafts/image_write.c'
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
c3, c4, c2 = 'x + 0x4000 < first', '(len & 0x3fff) > 0x3fff', 'x > first + 0x4000'
PAGES = '''			pages = len / 512;
			if (len % 512)
				pages++;
'''
T = "		t = type - '1';\n		partial = type != 0 && type != '0' && len < 0x4000;\n"
NX = '''			if (next != 0 && next != 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			}
'''
def m(cs, body, op='||'):
    return '		if (' + (' %s ' % op).join(cs) + ')\n			' + body + ';\n'
AXES = [
 [('opt', []), ('noopt', [(A, 'void writeFsTable')])],
 [('', []), ('no2', [(A2, '')]),
  ('2b', [(A2, m([c2], 'blocks++'))]),
  ('2s', [(A2, m([c2], 'start++'))]),
 ],
 [('', []),
  ('m1', [(M, m([c4, c3], 'blocks++'))]),
  ('m2', [(M, m([c3, c4], 'blocks += 2'))]),
  ('m3', [(M, m([c4, c3], 'blocks += 2'))]),
  ('m4', [(M, m([c3, c4], 'start++'))]),
  ('m5', [(M, m([c4, c3], 'start++'))]),
  ('m6', [(M, m([c3, c4], 'off++'))]),
  ('m7', [(M, m([c3 , '(len & 0x3fff) >= 0x4000'], 'blocks++'))]),
 ],
 [('', []), ('p1', [(PAGES, '			pages = len % 512 ? len / 512 + 1 : len / 512;\n')])],
 [('', []), ('t1', [(T, "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n")])],
 [('', []),
  ('n2', [(NX, NX.replace('start - xb.fsStart + i', 'start + i - xb.fsStart'))]),
  ('n1', [(NX, '''			if (next == 0 || next == 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			}
''')]),
 ],
]
