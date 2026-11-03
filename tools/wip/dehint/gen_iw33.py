# attempt 2, on build/iw/a2/m2D.c: all three of imgAdd's loop dead tests merged (no empty asm); 4 lines left in writeFsTable.
BASE = 'build/iw/a2/m2D.c'
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
M = '		if (x + 0x4000 < first || x > first + 0x4000 || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
c2, c3, c4 = 'x > first + 0x4000', 'x + 0x4000 < first', '(len & 0x3fff) > 0x3fff'
def m(*cs, body='blocks++'):
    return '		if (' + ' || '.join(cs) + ')\n			' + body + ';\n'
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
A1 = '	if (x > first + 0x4000)\n		blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
AXES = [
 [('', []), ('noopt', [(A, 'void writeFsTable')])],
 [('', []),
  ('m3', [(M, m(c3, c4, c2))]),
  ('m1', [(M, m(c2, c3, c4))]),
  ('mb', [(M, m(c3, c2, c4, body='blocks += 2'))]),
  ('ms', [(M, m(c3, c2, c4, body='start++'))]),
  ('m3b', [(M, m(c3, c4, c2, body='blocks += 2'))]),
  ('m3s', [(M, m(c3, c4, c2, body='start++'))]),
 ],
 [('', []), ('p1', [(PAGES, '			pages = len % 512 ? len / 512 + 1 : len / 512;\n')])],
 [('', []), ('t1', [(T, "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n")])],
 [('', []),
  ('n2', [(NX, NX.replace('start - xb.fsStart + i', 'start + i - xb.fsStart'))]),
 ],
 [('', []), ('a1', [(A1, '	if (first + 0x4000 < x)\n		blocks += 2;\n')]), ('a1b', [(A1, '	if (x > first + 0x4000)\n		blocks++;\n')])],
 [('', []), ('a5', [(A5, '			if (first + 0x4000 < x)\n				blocks++;\n')]), ('a5b', [(A5, '			if (x > first + 0x4000)\n				blocks += 2;\n')])],
 [('', []), ('a6', [(A6, '		if (first > x + 0x4000)\n			start++;\n')]), ('a6b', [(A6, '		if (x + 0x4000 < first)\n			blocks++;\n')])],
]
