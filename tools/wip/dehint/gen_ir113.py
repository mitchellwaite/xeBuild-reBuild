"""getImageSmc: two logs at expand, the second not 'guarded' at profile_estimate: forms where the bad arm's first
block isn't the log (while loop, nested test on a PHI that VRP folds, two edges into it).  Whole-function sweep."""
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
F = {
    # a while: the arm's test is the header, log not first
    'w1': Z + f'while (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
    'w2': Z + f'while (addr != 0x800) {{ if (addr == 0x1000) break; {L} }}\n',
    # nested dead test on the PHI
    'n1': Z + f'if (addr != 0x800 && addr != 0x1000) {{ if (addr) {{ {L} }} }}\n',
    'n2': Z + f'if (addr) {{ if (addr != 0x800 && addr != 0x1000) {{ {L} }} }}\n',
    'n3': Z + f'if (addr != 0x800) {{ if (addr != 0x1000) {{ {L} }} }}\n',
    'n4': Z + f'if (addr != 0x800) {{ if (addr != 0x1000) {{ if (addr) {{ {L} }} }} }}\n',
    # bad flag
    'f1': 'int bad = 0;\n' + Z + f'if (addr != 0x800 && addr != 0x1000) bad = 1;\n if (bad) {{ {L} }}\n',
    'f2': Z + f'int ok = addr == 0x800 || addr == 0x1000;\n if (!ok) {{ {L} }}\n',
    'f3': Z + f'int bad = addr != 0x800 && addr != 0x1000;\n if (bad) {{ {L} }}\n',
    'f4': Z + f'int ok = 0;\n if (addr == 0x800 || addr == 0x1000) ok = 1;\n if (!ok) {{ {L} }}\n',
    'f5': Z + f'int ok = 0;\n if (addr == 0x800) ok = 1;\n if (addr == 0x1000) ok = 1;\n if (!ok) {{ {L} }}\n',
    # else-if chain
    'c1': f'if (!addr) {{ {L} }} else if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
    'c2': f'if (!addr) {{ {L} }} else if (addr == 0x800 || addr == 0x1000) {{ }} else {{ {L} }}\n',
    'c3': f'if (addr == 0x800 || addr == 0x1000) {{ }} else if (!addr) {{ {L} }} else {{ {L} }}\n',
    'c4': f'if (addr) {{ if (addr != 0x800 && addr != 0x1000) {{ {L} }} }} else {{ {L} }}\n',
    # the one-log forms, for comparison
    'o1': f'if (!addr || (addr != 0x800 && addr != 0x1000)) {{ {L} }}\n',
    'o2': f'if (addr) {{ if (addr == 0x800 || addr == 0x1000) goto bback; }}\n {L} bback:\n',
}
B0 = '	bhot: __attribute__((hot));\n'
AX = []
for k, v in F.items():
    AX.append((k, [(A, v), (TAIL, '}\n')]))
AXES = [AX,
        [('at', []), ('a0', [(ATTR, 'void getImageSmc')])],
        [('sh', []), ('s0', [(SH, '')])],
        [('un', []), ('u0', [(UN, '')])],
        [('pn', []), ('p0', [(PIN, '	}\n')])],
        ]
