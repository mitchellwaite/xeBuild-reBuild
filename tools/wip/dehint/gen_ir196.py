"""irwin3: fsGetFile without pin_v, base build/ir/a13/fne.c (`fsFind(...) != 1`): window of each test (attempt 13)."""
FN = '_fsGetFile'
REMOVE = []
PS = list(range(50, 100, 2))
E = '__builtin_expect(!!(%s), 1)'
def W(c):
    return E % c
LOOP = 'while (left > 0x4000) {\n		memcpy(p + done, xb.dump + off, 0x4000);\n		left -= 0x4000;\n		done += 0x4000;\n		block = SWAP16(fs->map[block]) & 0x1fff;\n		off = fsOffset + (block << 14);\n	}\n	if (left)\n		memcpy(p + done, xb.dump + off, left);\n	*buf = p;'
TESTS = {
 'v': ('	if (v != 1)\n		return 0;\n	if (fsFind', '	if (' + W('v != 1') + ')\n		return 0;\n	if (fsFind'),
 'find': ('if (fsFind(name, &block, &len, &t, 1) != 1)\n', 'if (' + W('fsFind(name, &block, &len, &t, 1) != 1') + ')\n'),
 'nfind': ('if (fsFind(name, &block, &len, &t, 1) != 1)\n', 'if (!' + W('fsFind(name, &block, &len, &t, 1) == 1') + ')\n'),
 'loop': (LOOP, LOOP.replace('while (left > 0x4000)', 'while (' + W('left > 0x4000') + ')')),
 'nloop': (LOOP, LOOP.replace('while (left > 0x4000)', 'while (!' + W('left <= 0x4000') + ')')),
 'left': (LOOP, LOOP.replace('if (left)', 'if (' + W('left') + ')')),
 'nleft': (LOOP, LOOP.replace('if (left)', 'if (!' + W('!left') + ')')),
}
