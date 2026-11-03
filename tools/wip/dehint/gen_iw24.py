# attempt 2, on drafts/image_write.c: no __builtin_expect on the fits test.  With a call in both arms' first blocks
# PRED_CALL fires 71/29 and cancels to the 50% the expect gives, so the dead abort test can't be the arm's first block.
BASE = 'tools/wip/dehint/drafts/image_write.c'
TEST = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
C = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
B1 = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
B2 = '		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);\n'
B3 = '		strcpy(fsFiles[nFsFiles].name, name);\n'
B4 = '		fsFiles[nFsFiles].time = *time;\n'
ALL = C + B1 + B2 + B3 + B4
AXES = [
 [('nx', [(TEST, '	if (lim >= off + len) {\n')]),
  ('x', [])],
 [('', []),
  ('p0', [(ALL, B1 + B2 + B3 + B4)]),
  ('p1', [(ALL, B1 + C + B2 + B3 + B4)]),
  ('p2', [(ALL, B1 + B2 + C + B3 + B4)]),
  ('p3', [(ALL, B1 + B2 + B3 + C + B4)]),
  ('p4', [(ALL, B1 + B2 + B3 + B4 + C)]),
  ('p5', [(ALL, B3 + C + B1 + B2 + B4)]),
  ('p6', [(ALL, B3 + B1 + C + B2 + B4)]),
  ('p7', [(ALL, B3 + B1 + B2 + B4)]),
  ('p8', [(ALL, B3 + B1 + B2 + B4 + C)]),
 ],
]
