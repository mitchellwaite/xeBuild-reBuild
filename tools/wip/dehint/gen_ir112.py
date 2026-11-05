"""getImageSmc: zero arm inline (string first, literal 0) and a bad arm with two predecessors at profile_estimate (no PRED_CALL), the second from a test VRP folds (addr is 0x1000 or nonzero there), which fre1 can't."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
A = '''	if (!addr) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	} else {
		vhot: __attribute__((hot));
	}
	if (addr != 0x800 && addr != 0x1000)
		goto bad;
bback:
'''
TAIL = '''	return;
bad:
	bhot: __attribute__((hot));
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto bback;
}
'''
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
SH = '		shot: __attribute__((hot));\n'
UN = '''			if (!h)
				__builtin_unreachable();
'''
PIN = '''	} else
		__asm__("" : "+D"(addr));
'''
EX = 'if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
ZE = f'if (!addr) {{ {L} goto bback; }}\n'
F = {
    'e1': (Z + 'if (!addr) goto bad;\n if (addr != 0x800 && addr != 0x1000) goto bad;\n bback:\n', 1),
    'e2': (Z + 'if (addr == 0) goto bad;\n if (addr != 0x800) { if (addr != 0x1000) goto bad; }\n bback:\n', 1),
    'e3': (Z + 'if (addr <= 0) goto bad;\n if (addr != 0x800 && addr != 0x1000) goto bad;\n bback:\n', 1),
    'e4': (Z + 'if (addr < 0) goto bad;\n if (addr != 0x800 && addr != 0x1000) goto bad;\n bback:\n', 1),
    'i1': (Z + f'if (addr) {{ if (addr == 0x800 || addr == 0x1000) goto bback; }}\n {L} bback:\n', 0),
    'i2': (Z + f'if (!addr) goto fix;\n if (addr != 0x800 && addr != 0x1000) {{ fix: {L} }}\n bback:\n', 0),
    'i3': (Z + f'if (!addr) goto fix;\n if (addr == 0x800 || addr == 0x1000) goto bback;\n fix: {L} bback:\n', 0),
}
B0 = '	bhot: __attribute__((hot));\n'
AX = []
for k, (v, keep) in F.items():
    AX.append((k, [(A, v), (B0, '')] if keep else [(A, v), (TAIL, '}\n')]))
AXES = [AX,
        [('at', []), ('a0', [(ATTR, 'void getImageSmc')])],
        [('sh', []), ('s0', [(SH, '')])],
        [('un', []), ('u0', [(UN, '')])],
        [('pn', []), ('p0', [(PIN, '	}\n')])],
        [('ex', []), ('e0', [(EX, 'if (addr < 528 * xb.dumpPages) {')])]]
