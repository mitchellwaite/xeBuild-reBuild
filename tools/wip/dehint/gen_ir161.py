"""getImageSmc from gen_ir155's near miss: B needs the bad path's forwarder not merged with the zero path's at PRE (cse's EBB then runs past the log with addr live out).  Forms that thread one path late or not at all: switches on the tests, zero arm spellings."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
LL = LOG0 + ' addr = 0x1000;\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
A38 = f'size = 0x3800; {S3800}'
A30 = f'size = 0x3000; {S3000}'
PIN = '__asm__("" : "+D"(addr));'
k = OLD.index('if (!addr)')
e = OLD.index('unsigned t = addr;')
HEAD = OLD[:k]
Z0 = OLD[k:e]
e2 = OLD.index('return;\nbad:')
SA = OLD[OLD.index('if (t && addr'):e2]
Z = {
 'zi': Z0,
 'zs': f'switch (addr) {{ case 0: {LL} }}\n',
 'zs2': f'switch (addr) {{ case 0: {LL} break; default: break; }}\n',
 'zg': f'if (addr) goto nz; {LL} nz:;\n',
 'za': f'if (!addr) {{ {LOG0} addr += 0x1000; }}\n',
 'zt': f'if (!addr) {{ {LOG0} }}\n addr = addr ? addr : 0x1000;\n',
}
T = {
 'tn': 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\n',
 'ts': 'unsigned t = addr;\n switch (t) { case 0x800: case 0x1000: break; default: goto bad; }\n',
 'tu': 'unsigned t = addr;\n if (t != 0x1000) { switch (t) { case 0x800: break; default: goto bad; } }\n',
}
ARM = {
 'ai': f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}',
 'au': f'switch ((unsigned)addr) {{ case 0x800: {A38} break; default: {A30} break; }}',
 'ad': f'switch (addr) {{ case 0x800: {A38} break; default: {A30} break; }}',
 'at': f'if (t == 0x800) {{ {A38} }} else {{ {A30} }}',
}
B = {
 'bk': f'bad:\n{LL}goto bback;\n',
 'bt': f'bad:\n{LOG0} addr = 0x1000; t = addr;\n goto bback;\n',
 'bs': f'bad:\n{LOG0} addr = 0x1000; t = 0x1000;\n goto bback;\n',
}
AX = []
for kz, z in Z.items():
    for kt, t in T.items():
        for ka, a in ARM.items():
            for kb, b in B.items():
                AX.append(('.'.join((kz, kt, ka, kb)), [(OLD, HEAD + z + t + 'bback:\nif (size != 0x3000 && size != 0x3800) {' + a + '} else {' + PIN + '}\n' + SA + 'return;\n' + b + '}\n\n')]))
AXES = [AX]
