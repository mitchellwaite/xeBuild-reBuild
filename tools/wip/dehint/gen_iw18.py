# attempt 2, on src/image_write.c: pin_end removed, `end` kept alive by real uses (the fits test or the
# dead tests that stay anyway) rather than by the asm.
PIN = '	__asm__("" :: "g"(end));\n'
LEN = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
TEST = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
C1 = '		if ((len & 0x3fff) > 0x3fff) {\n			c1: __attribute__((cold));\n'
AXES = [
 [('nopin', [(PIN, '')])],
 [('', []),
  ('L1', [(LEN, '	if ((end & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L2', [(LEN, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L3', [(LEN, '	if (((off + len) & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L0', [(LEN, '')]),
 ],
 [('', []),
  ('T1', [(TEST, '	if (__builtin_expect(lim >= end, 1)) {\n')]),
  ('T2', [(TEST, '	if (__builtin_expect(end <= lim, 1)) {\n')]),
 ],
 [('', []),
  ('C1', [(C1, '		if ((end & 0x3fff) > 0x3fff) {\n			c1: __attribute__((cold));\n')]),
 ],
]
