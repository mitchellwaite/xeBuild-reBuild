"""getImageSmc, `ok &&` gone (gen_ir175's o.b.t.z): the limit or the out flag from an early-inlined helper, so its names are high; other ways to give the limit a late name."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('	if (ok && addr < 528 * xb.dumpPages)\n')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
BADA = OLD[OLD.index('badAddr:'):OLD.rindex('}')]
NL = chr(10)
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image' + chr(92) + 'n", addr, size);' + NL
TAIL = ' loadSmc(addr, size); return;' + NL + BADA + 'notSane:' + NL + NOT + '}' + NL + NL
OK1 = '		ok = 1;' + NL
L = '528 * xb.dumpPages'
HD = 'static void loadSmc(int addr, int size)' + NL
H0 = HD
H1 = 'static int dumpLimit(void)' + NL + '{' + NL + '	return 528 * xb.dumpPages;' + NL + '}' + NL + NL + HD
H2 = 'static int addrOutside(int addr)' + NL + '{' + NL + f'	return addr >= {L};' + NL + '}' + NL + NL + HD
H3 = 'static int addrInside(int addr)' + NL + '{' + NL + f'	return addr < {L};' + NL + '}' + NL + NL + HD
H4 = 'static uint32_t dumpLimit(void)' + NL + '{' + NL + '	return 528 * xb.dumpPages;' + NL + '}' + NL + NL + HD
H5 = H1
OUT = {
 'p': (H0, f'{{ int out = addr >= {L}; if (out > 0) goto notSane; }}'),
 'l1': (H1, '{ int out = addr >= dumpLimit(); if (out > 0) goto notSane; }'),
 'l2': (H1, '{ int lim = dumpLimit(); int out = addr >= lim; if (out > 0) goto notSane; }'),
 'o1': (H2, '{ int out = addrOutside(addr); if (out > 0) goto notSane; }'),
 'o2': (H2, 'if (addrOutside(addr) > 0) goto notSane;'),
 'o3': (H3, 'if (addrInside(addr) <= 0) goto notSane;'),
 'o4': (H3, '{ int in = addrInside(addr); if (in <= 0) goto notSane; }'),
 'l3': (H4, '{ int out = t >= dumpLimit(); if (out > 0) goto notSane; }'),
 'r1': (H0, f'{{ int left = {L} - addr; if (left <= 0) goto notSane; }}'),
 'r2': (H1, '{ int left = dumpLimit() - addr; if (left <= 0) goto notSane; }'),
}
AX = []
for k, (h, o) in OUT.items():
    AX.append((k, [(OLD, o + TAIL), (OK1, ''), (HD, h)]))
AXES = [AX]
