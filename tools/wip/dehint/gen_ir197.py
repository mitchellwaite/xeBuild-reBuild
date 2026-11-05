"""irwin3: fine window of fsGetFile's found test without pin_v (attempt 13)."""
FN = '_fsGetFile'
REMOVE = []
PS = list(range(68, 80))
E = '__builtin_expect(!!(%s), 1)'
TESTS = {
 'find': ('if (fsFind(name, &block, &len, &t, 1) != 1)\n', 'if (' + E % 'fsFind(name, &block, &len, &t, 1) != 1' + ')\n'),
 'nz': ('if (fsFind(name, &block, &len, &t, 1) != 1)\n', 'if (' + E % '!fsFind(name, &block, &len, &t, 1)' + ')\n'),
}
