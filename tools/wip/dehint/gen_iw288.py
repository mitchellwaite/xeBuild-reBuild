# attempt 23: `(off & 0x1ffff) / 512` computed before the block loop, so `256 - that` in the arm costs under LIM_EXPENSIVE: PRE's dead `(int)` cast stays in the arm at lim2's cleanup (dce4 removes it) and the arm survives as the forwarder, which swaps the two names unswitch frees. (LIM's cost rule is from memory; the dumps show the result.)
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw288.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
D0 = '	uint32_t i;\n\n	if (xb.rawSize < off'
D1 = '	uint32_t i;\n	uint32_t bo, bp;\n\n	if (xb.rawSize < off'
MEMC = '	memcpy(xb.hdr + off, src, len);\n'
LOOP = '	for (b = 0; b < blocks; b++) {\n		small ='
XOFF = '	x = off & 0x3fff;\n'
ARMS = [
 ('a1', '						left = (off & 0x1ffff) ? 256 - bp : 256;\n', '	bp = (off & 0x1ffff) / 512;\n'),
 ('a2', '						left = bo ? 256 - bp : 256;\n', '	bo = off & 0x1ffff;\n	bp = bo / 512;\n'),
 ('a3', '						left = 256;\n						if (off & 0x1ffff)\n							left -= bp;\n', '	bp = (off & 0x1ffff) / 512;\n'),
 ('a4', '						left = 256;\n						if (bo)\n							left -= bp;\n', '	bo = off & 0x1ffff;\n	bp = bo / 512;\n'),
]
PL = []
for lab, arm, d in ARMS:
    for wl, w in (('x', XOFF), ('m', MEMC), ('l', LOOP)):
        y = (d + w) if w != MEMC else (w + d)
        PL.append((lab + wl, [(L0, arm), (D0, D1), (w, y)]))
    PL.append((lab + 'e', [(L0, arm), (D0, D1), ('	x = off & 0x3fff;\n	start = (off - x) >> 14;\n', '	x = off & 0x3fff;\n	start = (off - x) >> 14;\n' + d)]))
AXES = [PL]
