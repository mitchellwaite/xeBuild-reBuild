# attempt 23: `(off & 0x1ffff) / 512` in the block loop's body, not the page loop's: LIM (from memory) only adds a dependency's cost when the def is in the same loop, so `256 - that` in the page loop's arm stays cheap and PRE's dead `(int)` cast stays in the arm at lim2's cleanup.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw291.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
D0 = '	uint32_t i;\n\n	if (xb.rawSize < off'
D1 = '	uint32_t i;\n	uint32_t bp;\n\n	if (xb.rawSize < off'
TOP = '	for (b = 0; b < blocks; b++) {\n		small ='
P0 = '		p = 0;\n		t = type - \'1\';\n'
PLOOP = '		for (end = p + npages; p < end; p++) {\n'
D = '		bp = (off & 0x1ffff) / 512;\n'
ARM = '						left = (off & 0x1ffff) ? 256 - bp : 256;\n'
ARM2 = '						if (off & 0x1ffff)\n							left = 256 - bp;\n						else\n							left = 256;\n'
ARM3 = '						left = 256;\n						if (off & 0x1ffff)\n							left -= bp;\n'
PL = []
for al, a in (('r', ARM), ('s', ARM2), ('t', ARM3)):
    PL.append((al + 'top', [(L0, a), (D0, D1), (TOP, '	for (b = 0; b < blocks; b++) {\n' + D + '		small =')]))
    PL.append((al + 'p0', [(L0, a), (D0, D1), (P0, D + P0)]))
    PL.append((al + 'p1', [(L0, a), (D0, D1), (P0, P0 + D)]))
    PL.append((al + 'pl', [(L0, a), (D0, D1), (PLOOP, D + PLOOP)]))
AXES = [PL]
