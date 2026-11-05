"""irwin3 on gen_ir175's p form (build/ir/gen_ir175_best.c): what P(not sane) does the prologue want?"""
FN = '_getImageSmc'
REMOVE = []
PS = list(range(50, 100, 2))
TESTS = {
 'out': ('if (out > 0) goto notSane;', 'if (__builtin_expect(out, 1)) goto notSane;'),
 'cmp': ('{ int out = addr >= 528 * xb.dumpPages; if (out > 0) goto notSane; }', 'if (__builtin_expect(addr >= 528 * xb.dumpPages, 1)) goto notSane;'),
 'cmp2': ('{ int out = addr >= 528 * xb.dumpPages; if (out > 0) goto notSane; }', 'if (__builtin_expect(528 * xb.dumpPages > addr, 0)) ; else goto notSane;'),
}
