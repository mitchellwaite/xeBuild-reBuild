"""Attempt 19: windows of single tests on the no-attribute draft (build/ir/a19/a0.c): what P stops ce3's one-insn hoist of edi = 0x1000 (measurement only)."""
FN = '_getImageSmc'
REMOVE = []
PS = list(range(3, 100, 3))
TESTS = {
    'ok': ('if (ok <= 0) {', 'if (__builtin_expect(!!(ok <= 0), 1)) {'),
    't': ('if (t != 0x1000) {', 'if (__builtin_expect(!!(t != 0x1000), 1)) {'),
    'wrong': ('if (wrong > 0)', 'if (__builtin_expect(!!(wrong > 0), 1))'),
    'bad': ('if (bad > 0) {', 'if (__builtin_expect(!!(bad > 0), 1)) {'),
    'o': ('if (o <= 0) {', 'if (__builtin_expect(!!(o <= 0), 1)) {'),
    'lim': ('if ((unsigned)addr != lim) {', 'if (__builtin_expect(!!((unsigned)addr != lim), 1)) {'),
    'out': ('if (out <= 0) {', 'if (__builtin_expect(!!(out <= 0), 1)) {'),
}
