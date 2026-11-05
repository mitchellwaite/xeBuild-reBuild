"""getImageSmc: `ok &&` gone, status-flag forms for the sane test on the current shape, attribute subsets and pin kept/off (attempt 14)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
FOCUS = ['_getImageSmc']
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
SANE = '''	if (ok && addr < 528 * xb.dumpPages)
		loadSmc(addr, size);
	else
		log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);
'''
NS = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
LS = 'loadSmc(addr, size);\n'
LIM = '528 * xb.dumpPages'
DECL = '	int bad, o;\n'
F = {
 'k': SANE,
 'f1': f'sane = 1; if (addr >= {LIM}) sane = 0; if (sane) {LS} else {NS}',
 'f2': f'sane = 1; if (addr >= {LIM}) sane = 0; if (!sane) {NS} else {LS}',
 'f3': f'sane = 0; if (addr < {LIM}) sane = 1; if (sane) {LS} else {NS}',
 'f4': f'sane = 0; if (addr < {LIM}) sane = 1; if (!sane) {NS} else {LS}',
 'f5': f'sane = addr < {LIM}; if (sane) {LS} else {NS}',
 'f6': f'sane = addr < {LIM}; if (!sane) {NS} else {LS}',
 'f7': f'sane = 1; if (addr >= {LIM}) sane = 0; if (!sane) {{ {NS} return; }} {LS}',
 'f8': f'sane = 0; if (addr < {LIM}) sane = 1; if (!sane) {{ {NS} return; }} {LS}',
 'f9': f'sane = ok; if (addr >= {LIM}) sane = 0; if (sane) {LS} else {NS}',
 'f10': f'if (addr >= {LIM}) ok = 0; if (ok) {LS} else {NS}',
 'f11': f'if (addr >= {LIM}) ok = 0; if (!ok) {NS} else {LS}',
 'f12': f'if (addr >= {LIM}) ok = 0; if (!ok) {{ {NS} return; }} {LS}',
 'f13': f'if (addr >= {LIM}) ok = 0; if (ok > 0) {LS} else {NS}',
 'f14': f'if (addr >= {LIM}) ok = 0; if (ok <= 0) {NS} else {LS}',
 'f15': f'ok = addr < {LIM}; if (ok) {LS} else {NS}',
 'f16': f'ok = 0; if (addr < {LIM}) ok = 1; if (ok) {LS} else {NS}',
 'f17': f'ok = 0; if (addr < {LIM}) ok = 1; if (!ok) {NS} else {LS}',
}
A = [('a3', []),
     ('a0', [(ATTR, 'void getImageSmc(void)')]),
     ('i2', [(ATTR, '__attribute__((optimize("no-if-conversion2"))) void getImageSmc(void)')]),
     ('tm', [(ATTR, '__attribute__((optimize("no-tree-tail-merge"))) void getImageSmc(void)')])]
PIN = '''	} else {
		__asm__("" : "+D"(addr));
	}
'''
P = [('p', []), ('np', [(PIN, '	}\n')])]
AXES = [[(k, [(SANE, v), (DECL, '	int bad, o, sane;\n')]) for k, v in F.items()], A, P]
