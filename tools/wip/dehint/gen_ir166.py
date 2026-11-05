"""getImageSmc: P(size bad) into [53, 70] with `bad > 0` (73) under an outer dead test folded in VRP1, attribute subsets."""
FOCUS = ['_getImageSmc']
BASE = 'build/ir/a10/xa3.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
i = src.index(A3)
j = src.index('void getImageKv(void)')
OLD = src[i:j]
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
PIN = '__asm__("" : "+D"(addr));'
k = OLD.index('if (size != 0x3000')
e = OLD.index('if (t && addr')
SZ = OLD[k:e]
BAD = 'int bad = size != 0x3000 && size != 0x3800;'
FORMS = {
 'ho': f'{{ {BAD} if (h) {{ if (bad > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'hi': f'{{ {BAD} if (bad > 0) {{ if (h) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'to': f'{{ {BAD} int nz = t != 0; if (nz > 0) {{ if (bad > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'ti': f'{{ {BAD} int nz = t != 0; if (bad > 0) {{ if (nz > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'hoe': f'{{ {BAD} if (h) {{ if (bad > 0) {{ {ARM} }} else {{ {PIN} }} }} else {{ {PIN} }} }}\n',
 'tn': f'{{ {BAD} if (t != 3) {{ if (bad > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'tn2': f'{{ {BAD} if (bad > 0) {{ if (t != 3) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
}
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM)}
AX = []
for kz, z in FORMS.items():
    for kq, q in ATTRS.items():
        AX.append((kz + '.' + kq, [(OLD, q + OLD.replace(A3, 'void getImageSmc(void)').replace(SZ, z))]))
AXES = [AX]
