"""getImageSmc: as gen_ir172, with the not-sane arm last before the return block (so the early return predictor fires only on the sane arm), badAddr's block moved before it."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('	if (ok && addr < 528 * xb.dumpPages)\n')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
BADA = OLD[OLD.index('badAddr:'):OLD.rindex('}')]
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image' + chr(92) + 'n", addr, size);' + chr(10)
L = '528 * xb.dumpPages'
TESTS = {
 'ge': f'addr >= {L}',
 'le': f'{L} <= addr',
 'nt': f'!(addr < {L})',
 'ug': f'(unsigned)addr >= {L}',
 'ga': f'!(t < {L})',
}
AX = []
for kt, c in TESTS.items():
    for kk, e in (('k', ()), ('d', (('		ok = 1;' + chr(10), ''),))):
        v = f'{{ int out = {c}; if (out > 0) goto notSane; }} loadSmc(addr, size); return;' + chr(10) + BADA + 'notSane:' + chr(10) + NOT + '}' + chr(10) + chr(10)
        AX.append((kt + '.' + kk, [(OLD, v)] + list(e)))
AXES = [AX]
