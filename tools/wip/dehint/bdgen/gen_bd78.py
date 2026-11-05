"""patchBlsBlmod without no-early-inlining: the patch walk as a static function (it holds calls, so it comes back at ipa-inline)."""
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
HEAD = 'void patchBlsBlmod(const void *blmod, int size)\n{'
DECL = '''	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;

	log_printf(1, "Patching BLs...");
'''
START = '	off = 0;\n	while (off < p->size) {\n		if (n != 2) {'
ENDM = '	if (blmod && size) {\n		log_printf(1, "Done!\\n");\n		if (!xb.cbb)'


def CASES_(t):
    a = t.index(START, t.index(HEAD))
    b = t.index(ENDM, a)
    return a, b


class F:
    pass


def make(kind):
    def f(t):
        a, b = CASES_(t)
        walk = t[a:b]
        h = t.index(HEAD)
        d = t.index(DECL, h)
        if kind == 'three':
            fn = 'static void applyPatches(int cd, int cbb, int pt)\n{\n	struct fileent *p = &xb.files[pt];\n	uint8_t *d = p->data;\n	uint32_t off, addr, len, i, t;\n	int n = 0;\n\n' + walk + '}\n\n'
            decl = '	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);\n	uint32_t off, i, max, end;\n\n	log_printf(1, "Patching BLs...");\n	applyPatches(cd, cbb, pt);\n'
        elif kind == 'two':
            fn = 'static void applyPatches(int cd, int cbb)\n{\n	struct fileent *p = &xb.files[findFile(23)];\n	uint8_t *d = p->data;\n	uint32_t off, addr, len, i, t;\n	int n = 0;\n\n' + walk + '}\n\n'
            decl = '	int cd = findFile(7), cbb = findFile(6);\n	uint32_t off, i, max, end;\n\n	log_printf(1, "Patching BLs...");\n	applyPatches(cd, cbb);\n'
        else:
            fn = 'static void applyPatches(int cd, int cbb, struct fileent *p)\n{\n	uint8_t *d = p->data;\n	uint32_t off, addr, len, i, t;\n	int n = 0;\n\n' + walk + '}\n\n'
            decl = '	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);\n	struct fileent *p = &xb.files[pt];\n	uint32_t off, i, max, end;\n\n	log_printf(1, "Patching BLs...");\n	applyPatches(cd, cbb, p);\n'
        return t[:h] + fn + t[h:d] + decl + t[b:]
    return f


def CASES(base):
    return [('nei_blmod', k, make(k)) for k in ('three', 'two', 'ptr')]
