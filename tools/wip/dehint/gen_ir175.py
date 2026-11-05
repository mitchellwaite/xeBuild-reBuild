"""getImageSmc: gen_ir174 base.d with flags that die in dce2 in other places, to move names at PRE (prephitmp must end below the limit's name)."""
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
BAD = '	bad = size != 0x3000 && size != 0x3800;' + NL
TT = '	if (t != 0x1000) {' + NL + '		if (t != 0x800)' + NL + '			goto badAddr;' + NL + '	}' + NL
assert BAD in src and TT in src
OUT = {
 'o': f'{{ int out = addr >= {L}; if (out > 0) goto notSane; }}',
 'o2': f'{{ int out = addr >= {L}; int in = !out; if (in <= 0) goto notSane; }}',
 'o3': f'{{ int in = addr < {L}; int out = !in; if (out > 0) goto notSane; }}',
}
B = {
 'b': BAD,
 'b2': '	{ int b1 = size != 0x3000; int b2 = size != 0x3800; bad = b1 && b2; }' + NL,
 'b3': '	{ int b1 = size != 0x3000; int b2 = size != 0x3800; bad = b1 & b2; }' + NL,
 'b4': '	{ int good = size == 0x3000 || size == 0x3800; bad = !good; }' + NL,
 'b5': '	bad = (size != 0x3000 && size != 0x3800) != 0;' + NL,
}
T = {
 't': TT,
 't1': '	if (t != 0x1000) {' + NL + '		int n = t != 0x800;' + NL + '		if (n != 0)' + NL + '			goto badAddr;' + NL + '	}' + NL,
 't2': '	{ int n = t != 0x1000; if (n != 0) {' + NL + '		if (t != 0x800)' + NL + '			goto badAddr;' + NL + '	} }' + NL,
 't3': '	{ int m = t != 0x800; int n = t != 0x1000; if (n != 0) {' + NL + '		if (m != 0)' + NL + '			goto badAddr;' + NL + '	} }' + NL,
}
Z = {
 'z': [],
 'z2': [('	if (ok <= 0) {', '	if (!(ok > 0)) {')],
 'z3': [('	int ok = addr != 0;' + NL, '	int zero = addr == 0, ok = !zero;' + NL)],
}
AX = []
for ko, o in OUT.items():
    for kb, b in B.items():
        for kt, t in T.items():
            for kz, z in Z.items():
                AX.append(('.'.join((ko, kb, kt, kz)), [(OLD, o + TAIL), (OK1, ''), (BAD, b), (TT, t)] + z))
AXES = [AX]
