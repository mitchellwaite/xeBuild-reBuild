"""checkBl split in two: size test in checkBl, the rest in a static function with calls inside, not early inlined and called once.  The call
is on the normal edge at profile_estimate (what blMagic does), and the attribute may go.  Combinations with the hot label, pins, blMagic."""
SZLOG = '	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
HEADA = '__attribute__((optimize("no-early-inlining")))\nint checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n	uint32_t blsize, c;\n	int m;\n'
BM = 'static void blMagic(const uint8_t *bl, int *m)\n{\n	*m = bl[0];\n}\n\n'


def CASE(text):
    return text


def transform(t, attr, hot, pint, pinm, bm, size_first):
    a = t.index('static void blMagic(')
    b = t.index('/* the bootloader', a) if False else t.index('int verifyBlSigs(void)', a)
    s = t[a:b]
    # the body between the size test and the error labels
    i = s.index('	switch (type) {')
    j = s.index('	return 0;\nbad:\n')
    sw = s[i:j]
    k = s.index('magic:\n')
    badlog = s[j + len('	return 0;\nbad:\n'):s.index('toobig:')]
    maglog = s[k:s.index('}\n\n', k)]
    # helpers before checkBl: crcSame etc. stay where they are
    pre = s[:s.index(HEADA.split('\n')[0])] if HEADA.split('\n')[0] in s else ''
    pre = pre.replace(BM, BM if bm else '')
    inner = ('__attribute__((optimize("no-early-inlining")))\n' if attr else '') + 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n	uint32_t c;\n	int m;\n\n'
    inner += ('	__asm__("" : : "D"(type));\n' if pint == 'in' else '')
    inner += ('	blMagic(bl, &m);\n' if bm else '	m = bl[0];\n')
    inner += ('	__asm__("" :: "a"(m));\n' if pinm else '')
    inner += '	if ((m & 0x43) != 0x43)\n		goto magic;\n' + sw + '	return 0;\nbad:\n' + badlog + maglog + '}\n\n'
    outer = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n	uint32_t blsize;\n\n'
    outer += ('	__asm__("" : : "D"(type));\n' if pint == 'out' else '')
    outer += '	blsize = getBeU32(bl + 12);\n'
    lab = 'toobig: __attribute__((hot));\n' if hot else ''
    if size_first:
        outer += '	if (blsize > size) {\n' + ('	' + lab if lab else '') + '	' + SZLOG + '		return -3;\n	}\n	return blCheckType(bl, blsize, type, crc);\n}\n\n'
    else:
        outer += '	if (blsize <= size)\n		return blCheckType(bl, blsize, type, crc);\n' + lab + SZLOG + '	return -3;\n}\n\n'
    return t[:a] + pre + inner + outer + t[b:]


BASE = 'build/bd/a3/base76.c'


def CASES(base):
    out = []
    for attr in (0, 1):
        for hot in (0, 1):
            for pint in ('', 'out', 'in'):
                for pinm in (0, 1):
                    for bm in (0, 1):
                        for sf in (0, 1):
                            def f(t, a=(attr, hot, pint, pinm, bm, sf)):
                                return transform(t, *a)
                            out.append(('', 'attr%d hot%d pt%s pm%d bm%d sf%d' % (attr, hot, pint, pinm, bm, sf), f))
    return out
