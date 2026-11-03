# attempt 2, on drafts/image_write_near.c: forms of the dead tests that stay anyway (free knobs, not
# in iwanneal.SHAPES).  Looking for the flip of writeFsTable's one compare; `noopt` also tries without opt.
BASE = 'tools/wip/dehint/drafts/image_write_near.c'
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
AXES = [
 [('', []), ('noopt', [(A, 'void writeFsTable')])],
 [('', []),
  ('a1a', [('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (first + 0x4000 < x)\n		blocks += 2;\n')]),
  ('a1b', [('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (x > first + 0x4000)\n		blocks++;\n')]),
  ('a1c', [('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (x > 0x4000 + first)\n		blocks = blocks + 2;\n')]),
  ('a1d', [('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (x > first + 0x4000) {\n		blocks++;\n		blocks++;\n	}\n')]),
 ],
 [('', []),
  ('a3a', [('		if (x + 0x4000 < first)\n			blocks++;\n', '		if (first > x + 0x4000)\n			blocks++;\n')]),
  ('a3b', [('		if (x + 0x4000 < first)\n			blocks++;\n', '		if (x + 0x4000 < first)\n			blocks += 2;\n')]),
  ('a3c', [('		if (x + 0x4000 < first)\n			blocks++;\n', '		if (first - 0x4000 > x)\n			blocks++;\n')]),
 ],
 [('', []),
  ('a4a', [('		if ((len & 0x3fff) > 0x3fff)\n			__asm__("");\n', '		if ((len & 0x3fff) >= 0x4000)\n			__asm__("");\n')]),
  ('a4b', [('		if ((len & 0x3fff) > 0x3fff)\n			__asm__("");\n', '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')]),
  ('a4c', [('		if ((len & 0x3fff) > 0x3fff)\n			__asm__("");\n', '		if ((len & 0x3fff) > 0x3fff)\n			continue;\n')]),
 ],
 [('', []),
  ('a5a', [('			if (x > first + 0x4000)\n				blocks++;\n', '			if (first + 0x4000 < x)\n				blocks++;\n')]),
  ('a5b', [('			if (x > first + 0x4000)\n				blocks++;\n', '			if (x > first + 0x4000)\n				blocks += 2;\n')]),
  ('a5c', [('			if (x > first + 0x4000)\n				blocks++;\n', '			if (x > first + 0x4000)\n				start++;\n')]),
 ],
 [('', []),
  ('a6a', [('		if (x + 0x4000 < first)\n			start++;\n', '		if (first > x + 0x4000)\n			start++;\n')]),
  ('a6b', [('		if (x + 0x4000 < first)\n			start++;\n', '		if (x + 0x4000 < first)\n			blocks++;\n')]),
  ('a6c', [('		if (x + 0x4000 < first)\n			start++;\n', '		if (x + 0x4000 < first)\n			start += 2;\n')]),
 ],
]
