"""getImageSmc 2-hint form (pin_addr, exp_smc; gen_ir130 v0.b0.t6.a0.s0.noa.ex, A and mov edi,ebx left): forms of the size test for P(size bad) just above 50, attribute options."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
def H(size_decl):
    return f'''{{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	{size_decl}
'''
SI = 'int size = SWAP32(h->smcBootSize);'
FORMS = {
 'and': (SI, f'if (size != 0x3000 && size != 0x3800) {{ {ARM} }} else {{ {PIN} }}'),
 'or': (SI, f'if (size == 0x3000 || size == 0x3800) {{ {PIN} }} else {{ {ARM} }}'),
 'orr': (SI, f'if (size == 0x3800 || size == 0x3000) {{ {PIN} }} else {{ {ARM} }}'),
 'andr': (SI, f'if (size != 0x3800 && size != 0x3000) {{ {ARM} }} else {{ {PIN} }}'),
 'ns': ('int size = SWAP32(h->smcBootSize);\n unsigned s = size;', f'if (s != 0x3000) {{ if (s != 0x3800) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'ns8': ('int size = SWAP32(h->smcBootSize);\n unsigned s = size;', f'if (s != 0x3800) {{ if (s != 0x3000) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'nss': (SI, f'if (size != 0x3000) {{ if (size != 0x3800) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'ne': ('int size = SWAP32(h->smcBootSize);\n unsigned s = size;', f'if (s == 0x3000) {{ {PIN} }} else if (s == 0x3800) {{ {PIN} }} else {{ {ARM} }}'),
 'flag': (SI, f'int ok = size == 0x3000 || size == 0x3800; if (!ok) {{ {ARM} }} else {{ {PIN} }}'),
 'flag2': (SI, f'int bad = size != 0x3000 && size != 0x3800; if (bad) {{ {ARM} }} else {{ {PIN} }}'),
 'fl3': (SI, f'int ok = 0; if (size == 0x3000) ok = 1; if (size == 0x3800) ok = 1; if (!ok) {{ {ARM} }} else {{ {PIN} }}'),
 'fl4': (SI, f'int bad = 1; if (size == 0x3000 || size == 0x3800) bad = 0; if (bad) {{ {ARM} }} else {{ {PIN} }}'),
 'm3': (SI, f'if ((size & 0xfffff7ff) != 0x3000) {{ {ARM} }} else {{ {PIN} }}'),
}
AX = []
tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
for kf, (decl, code) in FORMS.items():
    for kt, ta in ATTRS.items():
        for kx, ex in (('ex', 1), ):
            AX.append(('.'.join((kf, kt)), [(OLD, ta + 'void getImageSmc(void)\n' + H(decl) + Z + T + code + '\n' + REST + tail)]))
AXES = [AX]
