"""getImageSmc: `bad > 0` on the size test (73) with zero's freq lowered: `ok` flag on the zero test (73 + call: 13%) that also feeds the outer test of the sane check, or an outer `h` test folded in VRP1 (freq stays).  Attribute subsets."""
FOCUS = ['_getImageSmc']
BASE = 'build/ir/a10/gt.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
i = src.index(A3)
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
k = OLD.index('if (!addr)')
e = OLD.index('unsigned t = addr;')
Z0 = OLD[k:e]
X0 = 'if (t && addr < 528 * xb.dumpPages)'
assert X0 in OLD
Z = {
 'ofl': (f'int ok = addr != 0; if (ok <= 0) {{ {LOG} ok = 1; }}\n', 'if (ok && addr < 528 * xb.dumpPages)'),
 'ofg': (f'int ok = addr != 0; if (ok > 0) {{ }} else {{ {LOG} ok = 1; }}\n', 'if (ok && addr < 528 * xb.dumpPages)'),
 'ofx': (f'int ok = addr != 0; if (ok <= 0) {{ {LOG} ok = 1; }}\n', 'if (ok > 0 && addr < 528 * xb.dumpPages)'),
 'hz': (f'if (h) {{ if (!addr) {{ {LOG} }} }}\n', X0),
 'hz2': (f'if (!addr) {{ if (h) {{ {LOG} }} }}\n', X0),
}
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM)}
AX = []
for kz, (z, x) in Z.items():
    for kq, q in ATTRS.items():
        AX.append((kz + '.' + kq, [(OLD, q + OLD.replace(A3, 'void getImageSmc(void)').replace(Z0, z).replace(X0, x))]))
AXES = [AX]
