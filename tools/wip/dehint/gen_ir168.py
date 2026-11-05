"""getImageSmc: `bad > 0` (73), one or two outer tests on h that VRP1 folds (block freqs stay): zero under bb19 (O), the 3800 arm under 2000 (ok block's alignment).  Attribute subsets."""
FOCUS = ['_getImageSmc']
BASE = 'build/ir/a10/xa3.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
i = src.index(A3)
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
PIN = '__asm__("" : "+D"(addr));'
k = OLD.index('if (!addr)')
e = OLD.index('if (t && addr')
e2 = OLD.index('return;\nbad:')
HEAD = OLD[:k].replace(A3, 'void getImageSmc(void)')
SA = OLD[e:e2]
TAIL = OLD[e2:]
BAD = 'int bad = size != 0x3000 && size != 0x3800;'
Z0 = f'if (!addr) {{ {LOG} }}\n'
ZH = f'if (h) {{ if (!addr) {{ {LOG} }} }}\n'
TT = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
TD = 't = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
S0 = f'{{ {BAD} if (bad > 0) {{ {ARM} }} else {{ {PIN} }} }}\n'
SI = f'{{ {BAD} if (bad > 0) {{ if (h) {{ {ARM} goto sz; }} }} {PIN} sz:; }}\n'
A30 = f'size = 0x3000; {S3000}'
A38 = f'size = 0x3800; {S3800}'
ARMS = {
 'a': ARM,
 'o1': f'int o = addr != 0x800; if (o > 0) {{ {A30} }} else {{ {A38} }}',
 'o2': f'int o = addr != 0x800; if (o <= 0) {{ {A38} }} else {{ {A30} }}',
 'o3': f'int o = addr == 0x800; if (o <= 0) {{ {A30} }} else {{ {A38} }}',
 'o4': f'int o = addr == 0x800; if (o > 0) {{ {A38} }} else {{ {A30} }}',
}
FORMS = {}
for ka, a in ARMS.items():
    FORMS[ka] = ZH + TT + f'{{ {BAD} if (bad > 0) {{ {a} }} else {{ {PIN} }} }}\n'
    FORMS[ka + 'n'] = Z0 + TT + f'{{ {BAD} if (bad > 0) {{ {a} }} else {{ {PIN} }} }}\n'
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM)}
AX = []
for kz, z in FORMS.items():
    for kq, q in ATTRS.items():
        AX.append((kz + '.' + kq, [(OLD, q + HEAD + z + SA + TAIL)]))
AXES = [AX]
