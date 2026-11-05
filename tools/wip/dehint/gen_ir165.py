"""getImageSmc: `bad > 0` on the size test (opcode positive: 73, one over the O limit) with P(zero) lowered by `nz > 0` (73 + call: 13%), attribute subsets."""
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
Z = {
 'z0': Z0,
 'gt': f'{{ int nz = addr != 0; if (nz > 0) {{ }} else {{ {LOG} }} }}\n',
 'le': f'{{ int nz = addr != 0; if (nz <= 0) {{ {LOG} }} }}\n',
 'lt': f'{{ int nz = addr != 0; if (nz < 1) {{ {LOG} }} }}\n',
 'zl': f'{{ int z = addr == 0; if (z > 0) {{ {LOG} }} }}\n',
}
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM)}
AX = []
for kz, z in Z.items():
    for kq, q in ATTRS.items():
        AX.append((kz + '.' + kq, [(OLD, q + OLD.replace(A3, 'void getImageSmc(void)').replace(Z0, z))]))
AXES = [AX]
