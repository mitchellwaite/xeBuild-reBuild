"""Attempt 19: windows on build/ir/a19/e1.c (E written after badAddr, by goto: its edge block falls through at ce3, no IF-CASE-1; no attribute, 4 loose).  Measurement only."""
FN = '_getImageSmc'
REMOVE = []
PS = list(range(2, 100, 2))
TESTS = {
    'ok': ('if (ok <= 0) {', 'if (__builtin_expect(!!(ok <= 0), 1)) {'),
    't': ('if (t != 0x1000) {', 'if (__builtin_expect(!!(t != 0x1000), 1)) {'),
    'wrong': ('if (wrong > 0)', 'if (__builtin_expect(!!(wrong > 0), 1))'),
    'bad': ('if (bad > 0) {', 'if (__builtin_expect(!!(bad > 0), 1)) {'),
    'o': ('if (o <= 0) {', 'if (__builtin_expect(!!(o <= 0), 1)) {'),
    'lim': ('if ((unsigned)addr != lim) {', 'if (__builtin_expect(!!((unsigned)addr != lim), 1)) {'),
    'out': ('if (out <= 0) {', 'if (__builtin_expect(!!(out <= 0), 1)) {'),
}
