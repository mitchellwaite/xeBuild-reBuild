# attempt 22: xmalloc, compiled. Forms of where the raw buffer comes from, plain malloc. Base build/iw/a22/pm.c (src with plain malloc).
# `IWB=build/iw/a22/pm.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw281.py -n 40 -t 4`
A = '	xb.raw = (uint8_t *)(mem = malloc(xb.rawSize));\n	if (!mem)\n		return -1;\n'
RI = '	raw = (uint8_t *)mem;\n'
FN = 'int finalizeImage(void)\n{'
def H(helper, alloc, ri=RI):
    return [(FN, helper + FN), (A, alloc), (RI, ri)]
RET = 'static void *allocRaw(void)\n{\n	return xb.raw = malloc(xb.rawSize);\n}\n\n'
RET2 = 'static uint8_t *allocRaw(void)\n{\n	void *m = malloc(xb.rawSize);\n\n	xb.raw = m;\n	return m;\n}\n\n'
OUT = 'static int allocRaw(void **out)\n{\n	*out = malloc(xb.rawSize);\n	xb.raw = *out;\n	return *out != 0;\n}\n\n'
BOOL = 'static int allocRaw(void)\n{\n	xb.raw = malloc(xb.rawSize);\n	return xb.raw != 0;\n}\n\n'
SZ = 'static void *allocRaw(uint32_t size)\n{\n	return xb.raw = malloc(size);\n}\n\n'
USE = '	if (!(mem = allocRaw()))\n		return -1;\n'
AXES = [[
 ('base', []),
 ('ret', H(RET, USE)),
 ('ret2', H(RET2, USE)),
 ('sz', H(SZ, '	if (!(mem = allocRaw(xb.rawSize)))\n		return -1;\n')),
 ('out', H(OUT, '	if (!allocRaw(&mem))\n		return -1;\n')),
 # read back through xb: after the alloc, after each later call. Real loads, so they show the cost of losing the stack copy
 ('bool0', H(BOOL, '	if (!allocRaw())\n		return -1;\n	mem = xb.raw;\n')),
 ('bool1', H(BOOL, '	if (!allocRaw())\n		return -1;\n', '	raw = xb.raw;\n')),
 ('xb1', [(A, '	xb.raw = malloc(xb.rawSize);\n	if (!xb.raw)\n		return -1;\n'), (RI, '	raw = xb.raw;\n')]),
 ('xb2', [(A, '	xb.raw = malloc(xb.rawSize);\n	if (!xb.raw)\n		return -1;\n	mem = xb.raw;\n')]),
 # realloc(NULL, n): whether 6.2 folds it to malloc, and when
 ('re0', [(A, '	xb.raw = (uint8_t *)(mem = realloc(0, xb.rawSize));\n	if (!mem)\n		return -1;\n')]),
 # integer forms
 ('int', [(A, '	mem = malloc(xb.rawSize);\n	xb.raw = mem;\n	if (!mem)\n		return -1;\n'),
          (RI, '	{ uint32_t a = (uint32_t)mem; raw = (uint8_t *)a; }\n')]),
 # union, in case the pointer goes through a view conversion
 ('un', [(A, '	union { void *v; uint8_t *p; uint32_t a; } u;\n	u.v = malloc(xb.rawSize);\n	mem = u.v;\n	xb.raw = u.p;\n	if (!mem)\n		return -1;\n'),
         (RI, '	raw = (uint8_t *)u.a;\n')]),
 ('un2', [(A, '	union { void *v; uint32_t a; } u;\n	xb.raw = (uint8_t *)(mem = malloc(xb.rawSize));\n	if (!mem)\n		return -1;\n	u.v = mem;\n'),
         (RI, '	u.a += 0;\n	raw = (uint8_t *)u.v;\n')]),
]]
