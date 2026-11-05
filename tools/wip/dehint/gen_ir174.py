"""getImageSmc: gen_ir173 ge.d; P(not sane) 80.9 is right.  cmp's operand order wants prephitmp's name below the limit's (free list at PRE), the prologue may follow from the names (partition numbers).  Spellings of the limit and of out."""
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
HD = 'int bad, o;' + NL
assert HD in src
OK1 = '		ok = 1;' + NL
ZT = '	if (ok <= 0) {'
F = {
 'base': ('', f'{{ int out = addr >= {L}; if (out > 0) goto notSane; }}'),
 'lim1': ('', f'{{ int lim = {L}; int out = addr >= lim; if (out > 0) goto notSane; }}'),
 'limu': ('', f'{{ unsigned lim = {L}; int out = addr >= lim; if (out > 0) goto notSane; }}'),
 'limt': (f'unsigned lim = {L};' + NL, f'{{ int out = addr >= lim; if (out > 0) goto notSane; }}'),
 'lims': ('int lim;' + NL, f'lim = {L}; {{ int out = addr >= lim; if (out > 0) goto notSane; }}'),
 'tmp1': ('', f'{{ unsigned a = addr; int out = a >= {L}; if (out > 0) goto notSane; }}'),
 'tmp2': ('', f'{{ int in = addr < {L}; int out = !in; if (out > 0) goto notSane; }}'),
 'tmp3': ('', f'{{ int in = addr < {L}; int out = 1 - in; if (out > 0) goto notSane; }}'),
 'tmp4': ('', f'{{ int in = addr < {L}; int out = in ^ 1; if (out > 0) goto notSane; }}'),
 'tmp5': ('', f'{{ int out = addr < {L} ? 0 : 1; if (out > 0) goto notSane; }}'),
 'tmp6': ('', f'{{ int out = 0; if (addr >= {L}) out = 1; if (out > 0) goto notSane; }}'),
 'tmp7': ('', f'{{ int out = 1; if (addr < {L}) out = 0; if (out > 0) goto notSane; }}'),
 'mm1': ('', f'{{ int pages = xb.dumpPages; int out = addr >= 528 * pages; if (out > 0) goto notSane; }}'),
 'mm2': ('', f'{{ unsigned pages = xb.dumpPages; int out = addr >= pages * 528; if (out > 0) goto notSane; }}'),
}
OKS = {
 'd': [(OK1, '')],
 'k': [],
 'n': [(OK1, ''), ('	int ok = addr != 0;' + NL, ''), (ZT, '	if ((addr != 0) <= 0) {')],
 'b': [(OK1, ''), ('	int ok = addr != 0;' + NL, ''), (ZT, '	{ int ok = addr != 0; if (ok <= 0) {'), ('		addr = 0x1000;' + NL + '	}' + NL + '	t = addr;', '		addr = 0x1000;' + NL + '	} }' + NL + '	t = addr;')],
}
AX = []
for k, (d, v) in F.items():
    for kk, e in OKS.items():
        AX.append((k + '.' + kk, [(OLD, v + TAIL), (HD, HD + d)] + list(e)))
AXES = [AX]
