"""getImageSmc, whole function, all hints off (no attribute, pin, dead test): status-flag forms as in copyMmcImage (set, then test: first test unpredicted, threading folds the second) (attempt 14)."""
import itertools
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
FOCUS = ['_getImageSmc']
src = open(BASE, newline='').read().replace('\r\n', '\n')
a = src.rindex('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)')
b = src.rindex('void getImageKv(void)')
OLD = src[a:b]
BLA = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
A = {
 # t, nested, goto later: as HEAD but with bad arm inline
 'in': 'if (!addr) { ' + BLA + ' addr = 0x1000; } else { if (addr != 0x1000) { if (addr != 0x800) { ' + BLA + ' addr = 0x1000; } } }\n',
 'tn': 'if (!addr) { ' + BLA + ' addr = 0x1000; } t = addr; if (t != 0x1000) { if (t != 0x800) { ' + BLA + ' addr = 0x1000; } }\n',
 'ok1': 'ok = 1; if (!addr) ok = 0; else if (addr != 0x800 && addr != 0x1000) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'ok2': 'ok = 1; if (!addr) ok = 0; if (addr != 0x800 && addr != 0x1000) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'ok3': 'ok = 1; if (addr != 0x800) { if (addr != 0x1000) ok = 0; } if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'ok4': 'ok = 0; if (addr) { if (addr == 0x800 || addr == 0x1000) ok = 1; } if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'ok5': 'ok = addr != 0; if (addr != 0x800 && addr != 0x1000) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'z1': 'if (!addr) { ' + BLA + ' addr = 0x1000; } ok = 1; if (addr != 0x800 && addr != 0x1000) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'z2': 'ok = 1; if (!addr) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; } ok = 1; if (addr != 0x800 && addr != 0x1000) ok = 0; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'z3': 'ok = addr != 0; if (!ok) { ' + BLA + ' addr = 0x1000; } ok = addr == 0x800 || addr == 0x1000; if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
 'z4': 'if (!addr) { ' + BLA + ' addr = 0x1000; } ok = 1; if (addr != 0x800) { if (addr != 0x1000) ok = 0; } if (!ok) { ' + BLA + ' addr = 0x1000; }\n',
}
L30 = 'size = 0x3000;\nlog_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
L38 = 'size = 0x3800;\nlog_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
ARM = 'if (addr == 0x800) { ' + L38 + ' } else { ' + L30 + ' }\n'
ARM2 = 'if (addr != 0x800) { ' + L30 + ' } else { ' + L38 + ' }\n'
S = {
 'and': 'if (size != 0x3000 && size != 0x3800) { %s }\n',
 'fl': 'good = 1; if (size != 0x3000 && size != 0x3800) good = 0; if (!good) { %s }\n',
 'fl2': 'good = size == 0x3000 || size == 0x3800; if (!good) { %s }\n',
 'bad': 'bad = size != 0x3000 && size != 0x3800; if (bad) { %s }\n',
 'bad0': 'bad = 0; if (size != 0x3000 && size != 0x3800) bad = 1; if (bad) { %s }\n',
 'nest': 'good = 1; if (size != 0x3000) { if (size != 0x3800) good = 0; } if (!good) { %s }\n',
}
SANE = {
 'pl': 'if (addr < 528 * xb.dumpPages) loadSmc(addr, size); else ' + 'log_printf(1, "SMC at 0x%%x of size 0x%%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n',
 'fl': 'sane = 1; if (addr >= 528 * xb.dumpPages) sane = 0; if (sane) loadSmc(addr, size); else ' + 'log_printf(1, "SMC at 0x%%x of size 0x%%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n',
 'fl2': 'sane = addr < 528 * xb.dumpPages; if (sane) loadSmc(addr, size); else ' + 'log_printf(1, "SMC at 0x%%x of size 0x%%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n',
 'fl3': 'sane = 0; if (addr < 528 * xb.dumpPages) sane = 1; if (!sane) ' + 'log_printf(1, "SMC at 0x%%x of size 0x%%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n' + ' else loadSmc(addr, size);\n',
 'fl4': 'sane = 1; if (addr >= 528 * xb.dumpPages) sane = 0; if (!sane) ' + 'log_printf(1, "SMC at 0x%%x of size 0x%%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n' + ' if (sane) loadSmc(addr, size);\n',
}
def fn(ad, s, arm, sn, pre):
    return '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	int ok, good, bad, sane;
	unsigned t;

	''' + A[ad] + (S[s] % arm) + (SANE[sn] % ()) + '''}

'''
AX = []
for ad, s, (armn, arm), sn in itertools.product(A, S, (('e', ARM), ('n', ARM2)), SANE):
    AX.append(('.'.join((ad, s, armn, sn)), [(OLD, fn(ad, s, arm, sn, ''))]))
AXES = [AX]
