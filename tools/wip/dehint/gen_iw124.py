# attempt 7: lnp2 gone on a7: npages' shapes x partial's forms x blk; sort key ignores writeFsTable (a local form or the dead test fixes that) and call-target shifts
import os
N = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
CALC = '''if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
F = {
 'n1': '		if (partial) {\n			' + CALC + '		} else\n			npages = 32;\n',
 'n2': '		npages = 32;\n		if (partial) {\n			' + CALC + '		}\n',
 'n3': '''		if (!partial)
			npages = 32;
		else if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
''',
 'n6': '''		npages = 32;
		if (partial)
			npages = len % 512 ? (len + 512) / 512 : len / 512;
''',
 'n8': '''		npages = 32;
		if (partial) {
			npages = len / 512;
			if (len % 512)
				npages = (len + 512) / 512;
		}
''',
 'n9': '''		if (partial)
			npages = len % 512 ? (len + 512) / 512 : len / 512;
		else
			npages = 32;
''',
 'nA': '''		if (partial) {
			npages = len / 512;
			if (len % 512)
				npages++;
		} else
			npages = 32;
''',
 'nB': '''		if (partial)
			npages = pages0;
		else
			npages = 32;
''',
}
SM = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"
BL = '		blk = start + b;\n'
U1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
DD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
D0 = '	uint32_t pg;\n'
AXES = [
 [(k, [(N, v)] + ([(BL, BL + "		pages0 = len % 512 ? (len + 512) / 512 : len / 512;\n"), (D0, D0 + '	uint32_t pages0;\n')] if k == 'nB' else [])) for k, v in F.items()],
 [('', []),
  ('p1', [(SM, "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n")]),
  ('p2', [(SM, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
  ('p3', [(SM, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
 ],
 [('', []), ('nb', [(BL, ''), (U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n')])],
 [('', []), ('ndd', [(DD, '')])],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a7.c')
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_imgAddFileAs', '_imgAddMobile', '_addSmcConfig', '_writeInitialHeader']
