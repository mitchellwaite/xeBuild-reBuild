"""getImageSmc, `ok &&` gone, attribute kept: size test on the mask with a flag (gen_ir180 bfm: cmp order right, prologue left).  Lattice to move reassoc's names."""
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
TT = '	if (t != 0x1000) {' + NL + '		if (t != 0x800)' + NL + '			goto badAddr;' + NL + '	}' + NL
OUT = {
 'o': f'{{ int out = addr >= {L}; if (out > 0) goto notSane; }}',
 'o2': f'{{ int out = addr >= {L}; int in = !out; if (in <= 0) goto notSane; }}',
 'o3': f'{{ int in = addr < {L}; int out = !in; if (out > 0) goto notSane; }}',
 'o4': f'{{ int in = addr < {L}; if (in <= 0) goto notSane; }}',
}
B = {
 'm': '	bad = (size & ~0x800) != 0x3000;' + NL + '	if (bad > 0) {' + NL,
 'm1': '	{ int m = size & ~0x800; bad = m != 0x3000; }' + NL + '	if (bad > 0) {' + NL,
 'm2': '	bad = size != 0x3000;' + NL + '	if (size == 0x3800) bad = 0;' + NL + '	if (bad > 0) {' + NL,
 'm3': '	bad = (size & 0xfffff7ff) != 0x3000;' + NL + '	if (bad > 0) {' + NL,
 'm4': '	bad = !((size & ~0x800) == 0x3000);' + NL + '	if (bad > 0) {' + NL,
 'm5': '	bad = (size & ~0x800) == 0x3000;' + NL + '	if (bad <= 0) {' + NL,
 'm6': '	bad = size == 0x3000 || size == 0x3800;' + NL + '	if (bad <= 0) {' + NL,
 'm7': '	bad = (size != 0x3000) & (size != 0x3800);' + NL + '	if (bad > 0) {' + NL,
}
T = {
 't': TT,
 't1': '	if (t != 0x1000) {' + NL + '		int n = t != 0x800;' + NL + '		if (n != 0)' + NL + '			goto badAddr;' + NL + '	}' + NL,
 't2': '	{ int n = t != 0x1000; if (n != 0) {' + NL + '		if (t != 0x800)' + NL + '			goto badAddr;' + NL + '	} }' + NL,
 't3': '	{ int m = t != 0x800; int n = t != 0x1000; if (n != 0) {' + NL + '		if (m != 0)' + NL + '			goto badAddr;' + NL + '	} }' + NL,
}
Z = {
 'z': [],
 'z3': [(OKD, '	int zero = addr == 0, ok = !zero;' + NL)],
 'z4': [(OKD, '	int zero = addr == 0;' + NL), (OKT, '	if (zero > 0) {' + NL)],
}
O = {
 'of': [],
 'of2': [(OD, '		o = addr == 0x800;' + NL + '		if (o > 0) {' + NL)],
 'op': [(OD, '		if (addr == 0x800) {' + NL)],
}
AX = []
for ko, o in OUT.items():
    for kb, b in B.items():
        for kt, t in T.items():
            AX.append(('.'.join((ko, kb, kt)), [(OLD, o + TAIL), (OK1, ''), (BAD, b), (TT, t)]))
AXES = [AX, [(k, v) for k, v in Z.items()], [(k, v) for k, v in O.items()]]
