"""irwin3: fsGetFile without pin_v, natural found test: the copy loop's probability, the guess being that off's frequency can fall there rather than at the found test (attempt 13)."""
FN = '_fsGetFile'
REMOVE = []
PS = list(range(80, 100))
E = '__builtin_expect(!!(%s), 1)'
TESTS = {
 'loop': ('	while (left > 0x4000) {\n		memcpy(p + done', '	while (' + E % 'left > 0x4000' + ') {\n		memcpy(p + done'),
}
