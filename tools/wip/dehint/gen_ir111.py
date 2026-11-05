"""getImageSmc after gen_ir110: the one arm written inline (string first), reached by two edges; then a second log for the literal 0.  Other hints in a lattice."""
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
L0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", 0);\n addr = 0x1000;\n'
F = {
    # one arm inline
    'i1': f'if (addr) {{ if (addr == 0x800 || addr == 0x1000) goto ok; }}\n {L} ok:\n',
    'i2': f'if (addr) {{ if (addr == 0x800) goto ok; if (addr == 0x1000) goto ok; }}\n {L} ok:\n',
    'i3': f'if (!addr) goto fix;\n if (addr != 0x800 && addr != 0x1000) {{ fix: {L} }}\n',
    'i4': f'if (!addr) goto fix;\n if (addr == 0x800 || addr == 0x1000) goto ok;\n fix: {L} ok:\n',
    # two logs, second reached by goto from a test of its own
    't1': f'if (!addr) {{ {L} }} else {{ if (addr == 0x800 || addr == 0x1000) goto ok; {L} }}\n ok:\n',
    't2': f'if (!addr) {{ {L} goto ok; }}\n if (addr == 0x800 || addr == 0x1000) goto ok;\n {L} ok:\n',
    't3': f'if (!addr) {{ {L} }}\n if (addr == 0x800 || addr == 0x1000) goto ok;\n {L} ok:\n',
}
F2 = {'or': '	if (!addr || (addr != 0x800 && addr != 0x1000))\n		goto bad;\nbback:\n'}
B0 = '	bhot: __attribute__((hot));\n'
AXES = [[(k, [(A, v), (TAIL, '}\n')]) for k, v in F.items() if k[0] == 't'] + [(k, [(A, v), (B0, '')]) for k, v in F2.items()],
        [('at', []), ('a0', [(ATTR, 'void getImageSmc')])],
        [('sh', []), ('s0', [(SH, '')])],
        [('un', []), ('u0', [(UN, '')])],
        [('pn', []), ('p0', [(PIN, '	}\n')])],
        [('ex', []), ('e0', [(EX, 'if (addr < 528 * xb.dumpPages) {')])]]
