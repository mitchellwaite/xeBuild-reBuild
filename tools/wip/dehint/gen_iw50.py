# attempt 4: the one writeFsTable compare in near3 (IWB= base): order of writeFsTable's two imgAdd calls x forms of the type arms that
# die in writeFsTable's copies (real operations, folded only after inlining) x the optimize attribute.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
CALLS = '''	if (!xb.bigBlock)
		goto small;
	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);
	goto done;
small:
	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);
done:
'''
S12 = '''				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					if (type != 0x2a && type != 0x2c) {
'''
B2 = '''						if (type == 0x2c)
							s[5] = 1;
						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
'''
SM = '''					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					s[9] = 32 - pages;
					s[2] = 1;
					if (type != '0') {
						s[8] = len >> 8;
						s[7] = len;
					}
'''
AXES = [
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
 [('', []),
  ('c1', [(CALLS, '	if (xb.bigBlock)\n		imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n')]),
  ('c2', [(CALLS, '	if (!xb.bigBlock)\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n')]),
  ('c3', [(CALLS, '	if (xb.bigBlock)\n		goto big;\n	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n	goto done;\nbig:\n	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\ndone:\n')]),
  ('c4', [(CALLS, '	imgAdd(off, buf, i * 0x400, xb.bigBlock ? 0x2c : 0x30, xb.bigBlock ? 0x1ffe : 0x1ffd, 0);\n')]),
 ],
 [('', []),
  ('s1', [(S12, S12.replace('s[12] = (s[12] & 0xc0) | (type & 0x3f);', 's[12] = (type & 0x3f) | (s[12] & 0xc0);'))]),
  ('s2', [(S12, S12.replace('type > 1', 'type >= 2'))]),
  ('s3', [(S12, S12.replace('type != 0x2a && type != 0x2c', 'type != 0x2c && type != 0x2a'))]),
  ('s4', [(S12, S12.replace('type != 0x2a && type != 0x2c', '(type & ~6) != 0x28'))]),
 ],
 [('', []),
  ('b1', [(B2, B2.replace('						if (type == 0x2c)\n							s[5] = 1;\n', '').replace('						s[7] = xb.spare7;\n', '						s[7] = xb.spare7;\n						if (type == 0x2c)\n							s[5] = 1;\n'))]),
  ('b2', [(B2, B2.replace('if (type == 0x2c)', 'if (type != 0x2a)'))]),
 ],
 [('', []),
  ('m1', [(SM, SM.replace("type != '0'", "type > '0' || type < '0'"))]),
  ('m2', [(SM, SM.replace('					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n', '					s[12] = (type & 0x3f) | (s[12] & 0xc0);\n'))]),
 ],
]
