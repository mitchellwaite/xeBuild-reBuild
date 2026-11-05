"""getImageSmc: a lattice for a partial landing: t6's nested addr test (vhot, bhot gone) with subsets of the other hints."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
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
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
SH = '		shot: __attribute__((hot));\n'
UN = '''			if (!h)
				__builtin_unreachable();
'''
F = {
    't6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
    't7': Z + f'unsigned t = addr;\n if (t != 0x800) {{ if (t != 0x1000) {{ {L} }} }}\n',
}
AXES = [
    [(k, [(A, v), (TAIL, '}\n')]) for k, v in F.items()],
    [('a3', []), ('a0', [(ATTR, 'void getImageSmc')]),
     ('tm', [(ATTR, '__attribute__((optimize("no-tree-tail-merge"))) void getImageSmc')]),
     ('if2', [(ATTR, '__attribute__((optimize("no-if-conversion2"))) void getImageSmc')]),
     ('tmif2', [(ATTR, '__attribute__((optimize("no-tree-tail-merge", "no-if-conversion2"))) void getImageSmc')])],
    [('sh', []), ('s0', [(SH, '')])],
    [('un', []), ('u0', [(UN, '')])],
]
