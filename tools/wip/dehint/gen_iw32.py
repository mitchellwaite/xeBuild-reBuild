# attempt 2, on drafts/image_write.c: plain-C bodies for the remaining empty asm in imgAdd's dead test add2 (count unchanged, but no asm)
BASE = 'tools/wip/dehint/drafts/image_write.c'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
c = 'x > first + 0x4000'
B = ['first++', 'x++', 'continue', 'break', 'blocks--', 'b++', 'start++', 'start--', 'first = 0', 'x = 0', 'blocks = 1', 'tail++', 'tail = 0', 'pad = 0',
     'type = 0', 'next = 0', 'src = 0', 'abort()', 'memset(xb.hdr, 0, 1)', 'log_printf(0, "x")', 'return -1', 'blocks *= 2', 'b = 0', 'b--']
V = [(('b%d' % i), [(A2, '		if (%s)\n			%s;\n' % (c, b))]) for i, b in enumerate(B)]
V += [(('c%d' % i), [(A2, '		if (first + 0x4000 < x)\n			%s;\n' % b)]) for i, b in enumerate(B)]
V += [('m1', [(A2 + M, '		if (x > first + 0x4000 || x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n')]),
      ('m2', [(A2 + M, '		if (x + 0x4000 < first || x > first + 0x4000 || (len & 0x3fff) > 0x3fff)\n			blocks++;\n')]),
      ('m3', [(A2 + M, '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff || x > first + 0x4000)\n			blocks++;\n')]),
      ('m4', [(A2 + M, '		if (x + 0x4000 < first)\n			blocks++;\n		if ((len & 0x3fff) > 0x3fff || x > first + 0x4000)\n			blocks++;\n')]),
      ('m5', [(A2 + M, '		if ((len & 0x3fff) > 0x3fff || x > first + 0x4000)\n			blocks++;\n		if (x + 0x4000 < first)\n			blocks++;\n')]),
      ('m6', [(A2 + M, '		if ((len & 0x3fff) > 0x3fff || x > first + 0x4000 || x + 0x4000 < first)\n			blocks++;\n')]),
      ]
AXES = [V]
