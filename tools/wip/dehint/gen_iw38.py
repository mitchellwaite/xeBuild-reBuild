# attempt 3: a1 and c3 gone.  `first + 0x4000` as a local computed where a1's test computed it (before memcpy), used by the remaining dead tests:
# keeps a1's name (_16) without its test.  Also where `x + 0x4000` comes from for a6.
BASE = 'build/iw/a3/b6.c'
D = '	memcpy(xb.hdr + off, src, len);\n	if (pad == 1) if (tail)\n'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
A5 = '			if (x > first + 0x4000)\n				blocks += 2;\n'
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
V = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n'
HI = '	hi = first + 0x4000;\n'
AXES = [
 [('', []),
  ('hi', [(V, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, hi;\n'), (D, HI + D), (A2, '		if (x > hi)\n			__asm__("");\n'), (A5, '			if (x > hi)\n				blocks += 2;\n')]),
  ('hi2', [(V, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, hi;\n'), (D, HI + D), (A2, '		if (x > hi)\n			__asm__("");\n')]),
  ('hi3', [(V, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, hi;\n'), (D, HI + D), (A5, '			if (x > hi)\n				blocks += 2;\n')]),
  ('hi4', [(V, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, hi;\n'), (D, D.replace('	if (pad', HI + '	if (pad')), (A2, '		if (x > hi)\n			__asm__("");\n'), (A5, '			if (x > hi)\n				blocks += 2;\n')]),
 ],
 [('', []),
  ('lo', [(V, '	uint32_t lo;\n' + V), (D, '	lo = x + 0x4000;\n' + D), (A6, '		if (lo < first)\n			start++;\n')]),
  ('lo2', [(A6, '		if (first > x + 0x4000)\n			start++;\n')]),
 ],
 [('', []), ('b1', [(A5, A5.replace('blocks += 2', 'blocks++'))])] if 0 else [('', [])],
 [('', []), ('i1', [('	uint32_t i;\n\n	if (xb.rawSize', '	uint32_t i;\n\n	blocks = 0;\n	if (xb.rawSize')])],
]
