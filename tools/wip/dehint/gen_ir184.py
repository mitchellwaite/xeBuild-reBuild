"""irwin3 on s4 (gen_ir183 s4gt, bad arm inline, out flag, sane arm returns early): windows of the tests."""
FN = '_getImageSmc'
REMOVE = []
PS = list(range(50, 100, 3))
TESTS = {
 'out': ('if (out <= 0) {', 'if (__builtin_expect(out, 1) <= 0) {'),
 'bad': ('if (bad > 0) {', 'if (__builtin_expect(bad, 1) > 0) {'),
 'zero': ('if (ok <= 0) {', 'if (__builtin_expect(!ok, 0)) {'),
 't8': ('		if (t != 0x800) {', '		if (__builtin_expect(t != 0x800, 1)) {'),
 't1': ('	if (t != 0x1000) {', '	if (__builtin_expect(t != 0x1000, 1)) {'),
 'o': ('if (o <= 0) {', 'if (__builtin_expect(!o, 1)) {'),
}
