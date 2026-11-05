"""irwin3: fsGetFile without pin_v."""
FN = '_fsGetFile'
REMOVE = [('	__asm__("" : : "S"(v));\n', '')]
E = '__builtin_expect(!!(%s), 1)'
def W(c):
    return E % c
TESTS = {
 'v': ('if (v != 1)\n		return 0;\n	if (!fsFind(name, &block, &len, &t, 1))', 'if (' + W('v != 1') + ')\n		return 0;\n	if (!fsFind(name, &block, &len, &t, 1))'),
 'find': ('if (!fsFind(name, &block, &len, &t, 1))\n		return 0;\n	off = fsOffset + (block << 14);\n	p = calloc', 'if (' + W('!fsFind(name, &block, &len, &t, 1)') + ')\n		return 0;\n	off = fsOffset + (block << 14);\n	p = calloc'),
 'loop': ('while (left > 0x4000) {\n		memcpy(p + done, xb.dump + off, 0x4000);\n		left -= 0x4000;\n		done += 0x4000;\n		block = SWAP16(fs->map[block]) & 0x1fff;\n		off = fsOffset + (block << 14);\n	}\n	if (left)\n		memcpy(p + done, xb.dump + off, left);\n	*buf = p;',
          'while (' + W('left > 0x4000') + ') {\n		memcpy(p + done, xb.dump + off, 0x4000);\n		left -= 0x4000;\n		done += 0x4000;\n		block = SWAP16(fs->map[block]) & 0x1fff;\n		off = fsOffset + (block << 14);\n	}\n	if (left)\n		memcpy(p + done, xb.dump + off, left);\n	*buf = p;'),
 'left': ('	if (left)\n		memcpy(p + done, xb.dump + off, left);\n	*buf = p;', '	if (' + W('left') + ')\n		memcpy(p + done, xb.dump + off, left);\n	*buf = p;'),
}
