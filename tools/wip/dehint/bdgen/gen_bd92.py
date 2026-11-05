"""Diagnostic: from the hint-free goto form (gen_bd91 goto split0 first), which frequencies are enough?  expects on each test (not to land)."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    f = g.fn('goto', 0, 'first')
    out = []
    for crc, sz, mag, arm, pin in itertools.product((0, 1), (0, 1, 2), (0, 1), (0, 1), (0, 1)):
        s = f
        if crc:
            s = s.replace('if (c != crc)', 'if (__builtin_expect(c != crc, 0))')
        if sz == 1:
            s = s.replace('toobig:\n', 'toobig: __attribute__((hot));\n')
        if sz == 2:
            s = s.replace('if (blsize > size)', 'if (__builtin_expect(blsize > size, 1))')
        if mag:
            s = s.replace('if ((m & 0x43) != 0x43)', 'if (__builtin_expect((m & 0x43) != 0x43, 0))')
        if arm:
            for c in 'BDEFGC':
                s = s.replace("if (bl[1] != '%s')" % c, "if (__builtin_expect(bl[1] != '%s', 0))" % c)
        if pin:
            s = s.replace('\tif ((m & 0x43)', '\t__asm__("" :: "a"(m));\n\tif ((m & 0x43)').replace('\tif (__builtin_expect((m & 0x43)', '\t__asm__("" :: "a"(m));\n\tif (__builtin_expect((m & 0x43)')
        out.append(('crc%d sz%d mag%d arm%d pin%d' % (crc, sz, mag, arm, pin), base[:a] + s + base[b:]))
    return out
