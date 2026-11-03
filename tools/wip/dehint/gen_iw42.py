# attempt 3: from the landed source: a1, c3 and the a2 asm each optional, with the moves that fixed the other functions in v2.c (t order, `end` in the len++ test,
# a2 with a plain body).  Anything identical with less than the landed count wins.
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A1 = '	if (x > first + 0x4000)\n		blocks += 2;\n'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
T = "		t = type - '1';\n		partial = type != 0 && type != '0' && len < 0x4000;\n"
LIM = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n'
L = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
AXES = [
 [('', []), ('A1', [(A1, '')])],
 [('', []), ('C3', [(M, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')])],
 [('', []), ('Ab2', [(A2, '		if (x > first + 0x4000)\n			blocks += 2;\n')]), ('Ab1', [(A2, '		if (x > first + 0x4000)\n			blocks++;\n')]),
  ('As', [(A2, '		if (x > first + 0x4000)\n			start++;\n')]), ('A0', [(A2, '')])],
 [('', []), ('t', [(T, "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n")])],
 [('', []), ('e', [(LIM, LIM + '	uint32_t end = off + len;\n'), (L, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n')])],
 [('', []), ('f2', [(A5, '			if (x > first + 0x4000)\n				blocks += 2;\n')])],
 [('', []), ('s1', [(A6, '		if (x + 0x4000 < first)\n			blocks++;\n')]), ('s2', [(A6, '		if (first > x + 0x4000)\n			start++;\n')])],
]
