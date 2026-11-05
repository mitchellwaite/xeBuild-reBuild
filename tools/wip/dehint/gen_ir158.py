"""getImageSmc from gen_ir155's near miss: attribute subsets against forms of the size test, for O (P(size bad) a bit over 50 wins bb-reorder's tie) with tail merge off."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
A38 = f'size = 0x3800; {S3800}'
A30 = f'size = 0x3000; {S3000}'
ARM = f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}'
PIN = '__asm__("" : "+D"(addr));'
k = OLD.index('if (size != 0x3000')
e = OLD.index('if (t && addr')
SZ = OLD[k:e]
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM)}
SIZES = {
 'if': SZ,
 'sh': f'if (size != 0x3000 && size != 0x3800) {{ shot: __attribute__((hot)); {ARM} }} else {{ {PIN} }}\n',
 'ns': f'{{ unsigned s = size; if (s != 0x3000) {{ if (s != 0x3800) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'ns2': f'{{ unsigned s = size; if (s != 0x3800) {{ if (s != 0x3000) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'ni': f'{{ int s = size; if (s != 0x3000) {{ if (s != 0x3800) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n',
 'nr': f'{{ unsigned s = size; if (s == 0x3000) goto ok; if (s == 0x3800) goto ok; {ARM} goto sz; ok: {PIN} sz:; }}\n',
 'sw': f'switch (size) {{ case 0x3000: case 0x3800: {PIN} break; default: {ARM} }}\n',
 'sw2': f'switch (size) {{ default: {ARM} break; case 0x3000: case 0x3800: {PIN} }}\n',
}
AX = []
for ks, s in SIZES.items():
    for kq, q in ATTRS.items():
        AX.append((ks + '.' + kq, [(OLD, q + OLD.replace(SZ, s))]))
AXES = [AX]
