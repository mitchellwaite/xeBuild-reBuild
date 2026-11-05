"""irwin3: goto form xio (gen_ir222), windows of ok0, ok1 tests after the clear (attempt 16; measurement only)."""
FN = '_findAnchor'
REMOVE = []
PS = list(range(5, 96, 3))
E = '__builtin_expect(!!(%s), 1)'
TESTS = {
 's0': ('if (ok0) goto sel0;', 'if (' + E % 'ok0' + ') goto sel0;'),
 's1': ('if (ok1) { log_printf(1, "anchor block v %d at 0x2fec000 is selected', 'if (' + E % 'ok1' + ') { log_printf(1, "anchor block v %d at 0x2fec000 is selected'),
 'cmp': ('{ if (v0 < v1) ok0 = 0;', '{ if (' + E % 'v0 < v1' + ') ok0 = 0;'),
}
