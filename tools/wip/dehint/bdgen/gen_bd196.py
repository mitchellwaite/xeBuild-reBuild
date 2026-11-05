"""exp_upd (attempt 8), a check of the mechanism: with the expect kept on the first pair, which partner X in (23|X) still gives the
reference's mask?  The claim is only 15: the other types are tested again in addUpdateBls' body, so FRE reuses the first block's
`type == X` there, the compare has two uses and reassoc leaves it out of the range test."""
OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'


def CASES(base):
    out = []
    for x in (15, 9, 10, 16, 24, 25):
        rest = [t for t in (16, 9, 10, 24, 25, 15) if t != x]
        s = 'return __builtin_expect(type == 23 || type == %d, 0) || %s;' % (x, ' || '.join('type == %d' % t for t in rest))
        out.append(('X=%d' % x, base.replace(OLD, s)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
