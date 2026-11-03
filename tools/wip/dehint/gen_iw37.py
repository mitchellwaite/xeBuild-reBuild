# attempt 3: imgAddFile without its expect.  PRED_CALL needs the guarded block dominated by the test, so an error block reached from
# two tests (a dead one first) gets no prediction from the second: 50/50 like the expect at --param 50.
FOCUS = ['_imgAddFile']
L = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
T = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
AB = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
D = '(len & 0x3fff) <= 0x3fff'
AXES = [
 [('', []), ('noL', [(L, '')])],
 [('', []), ('noAB', [(AB, '')]), ('c', [(AB, '		if ((len & 0x3fff) > 0x3fff)\n			len++;\n')])],
 [
  ('x', []),
  ('nx', [(T, '	if (lim >= off + len) {\n')]),
  ('d1', [(T, '	if (%s && lim >= off + len) {\n' % D)]),
  ('d2', [(T, '	if (lim >= off + len && %s) {\n' % D)]),
  ('d3', [(T, '	if (lim - len >= off && %s) {\n' % D)]),
  ('d4', [(T, '	if (len <= 0x3fff + (len & ~0x3fff) && lim >= off + len) {\n')]),
  ('d5', [(T, '	if (lim >= off + len && len <= 0x3fff + (len & ~0x3fff)) {\n')]),
  ('d6', [(T, '	if (off + len <= lim && %s) {\n' % D)]),
  ('d7', [(T, '	if (%s && off + len <= lim) {\n' % D)]),
 ],
]
