"""getImageSmc, `ok &&` gone, chain order of x.c (sane, not-sane, bad arm, return: s2 of gen_ir183), P(not sane) 73: the inner arms must stay under 10% of entry another way: malloc's test at 73 instead of pointer 85."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('	if (ok && addr < 528 * xb.dumpPages)\n')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
BADA = OLD[OLD.index('badAddr:'):OLD.rindex('}')]
NL = chr(10)
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image' + chr(92) + 'n", addr, size);' + NL
L = '528 * xb.dumpPages'
OK1 = '		ok = 1;' + NL
LOAD = 'loadSmc(addr, size);'
TAILS = {
 's2': '{ int out = addr >= ' + L + '; if (out <= 0) { ' + LOAD + ' return; } }' + NL + NOT + 'goto end;' + NL + BADA + 'end: ;' + NL + '}' + NL + NL,
 's5': '{ int out = addr >= ' + L + '; if (out > 0) ' + NOT + ' else ' + LOAD + ' }' + NL + 'return;' + NL + BADA + '}' + NL + NL,
 's6': '{ int in = addr < ' + L + '; if (in > 0) ' + LOAD + ' else ' + NOT + ' }' + NL + 'return;' + NL + BADA + '}' + NL + NL,
 's7': 'if (addr < ' + L + ') ' + LOAD + ' else ' + NOT + 'return;' + NL + BADA + '}' + NL + NL,
}
M = '	xb.smc.data = malloc(size);' + NL + '	if (xb.smc.data) {' + NL
assert M in src
MF = {
 'm0': [],
 'm1': [(M, '	xb.smc.data = malloc(size);' + NL + '	int got = xb.smc.data != 0;' + NL + '	if (got > 0) {' + NL)],
 'm2': [(M, '	int got;' + NL + '	xb.smc.data = malloc(size);' + NL + '	got = xb.smc.data != 0;' + NL + '	if (got > 0) {' + NL)],
}
AXES = [[(k, [(OLD, v), (OK1, '')]) for k, v in TAILS.items()], list(MF.items())]
