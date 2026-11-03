# attempt 3: near removal sets x the shapes that a single-shape probe showed moving writeFsTable's compares at small cost.
import importlib.util, os
_s = importlib.util.spec_from_file_location('g43', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw43.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
PAGES = '''			pages = len / 512;
			if (len % 512)
				pages++;
'''
NX = '''			if (next != 0 && next != 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			}
'''
TAIL = '''		if (rem < 0x4000)
			tail = rem;
		else
			tail = rem % 0x4000;
'''
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
STORE = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
TL = '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n'
SETS = [s for s in _m.SETS if s[0] in ('A0te', 'A1b2te', 'A1C3b2te', 'C3b2te')]
AXES = [
 SETS,
 [('', []),
  ('pg1', [(PAGES, '			pages = len % 512 ? len / 512 + 1 : len / 512;\n')]),
  ('pg3', [(PAGES, '			if (len % 512)\n				pages = len / 512 + 1;\n			else\n				pages = len / 512;\n')])],
 [('', []),
  ('nx2', [(NX, NX.replace('start - xb.fsStart + i', 'start + i - xb.fsStart'))])],
 [('', []),
  ('tl1', [(TAIL, '		tail = rem < 0x4000 ? rem : rem % 0x4000;\n')])],
 [('', []),
  ('pdu', [('	int partial;\n', '	uint8_t partial;\n')]),
  ('pdi', [('	int partial;\n', '	uint32_t partial;\n')])],
 [('', []),
  ('s2', [(A6, '		if (first > x + 0x4000)\n			start++;\n')]),
  ('sb', [(A6, '		if (x + 0x4000 < first)\n			blocks++;\n')])],
 [('', []),
  ('st', [(STORE, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('tl', [(TL, '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')]),
  ('sttl', [(STORE, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n'), (TL, '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')])],
]
