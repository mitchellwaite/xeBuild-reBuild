"""getImageSmc, `ok &&` gone (notSane at the end, out flag), attribute kept: fewer flags to change what forwprop3 frees above PRE's pops (need 1 or 2 fewer freed).
Axes: ok flag or plain; size test as flag, mask, plain &&; o flag or plain."""
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
TAIL = ' loadSmc(addr, size); return;' + NL + BADA + 'notSane:' + NL + NOT + '}' + NL + NL
OK1 = '		ok = 1;' + NL
OKD = '	int ok = addr != 0;' + NL
OKT = '	if (ok <= 0) {' + NL
BAD = '	bad = size != 0x3000 && size != 0x3800;' + NL + '	if (bad > 0) {' + NL
OD = '		o = addr != 0x800;' + NL + '		if (o <= 0) {' + NL
OUT = f'{{ int out = addr >= {L}; if (out > 0) goto notSane; }}'
AXES = [
 [('okf', [(OLD, OUT + TAIL), (OK1, '')]), ('okp', [(OLD, OUT + TAIL), (OK1, ''), (OKD, ''), (OKT, '	if (!addr) {' + NL)])],
 [('bf', []),
  ('bm', [(BAD, '	if ((size & ~0x800) != 0x3000) {' + NL)]),
  ('bm2', [(BAD, '	if ((size & 0xfffff7ff) != 0x3000) {' + NL)]),
  ('bma', [(BAD, '	bad = size & ~0x800;' + NL + '	if (bad != 0x3000) {' + NL)]),
  ('bfm', [(BAD, '	bad = (size & ~0x800) != 0x3000;' + NL + '	if (bad > 0) {' + NL)]),
  ('bp', [(BAD, '	if (size != 0x3000 && size != 0x3800) {' + NL)])],
 [('of', []), ('op', [(OD, '		if (addr == 0x800) {' + NL)])],
]
