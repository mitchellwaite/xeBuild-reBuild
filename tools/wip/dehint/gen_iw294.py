# attempt 23: local arrays in the nonzero arm that SRA can't take until a loop unrolls at cunrolli (so the scope clobber outlives lim2), by left's type and where the assignment to left sits relative to the clobber.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw294.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
D = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n	int left;\n'
TY = [
 ('', []),
 ('lu', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, left;\n')]),
 ('pi', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages;\n	int left, pages;\n')]),
]
def f(body, els='						} else\n							left = 256;\n'):
    return [(L0, '						if (off & 0x1ffff) {\n' + body + els)]
FO = [
 ('', []),
 ('f1', f('							uint32_t n[2];\n							int k;\n							n[0] = off & 0x1ffff;\n							n[1] = 512;\n							left = 256;\n							for (k = 0; k < 1; k++)\n								left -= n[k] / n[k + 1];\n')),
 ('f2', f('							uint32_t n[2];\n							uint32_t u = 256;\n							int k;\n							n[0] = off & 0x1ffff;\n							n[1] = 512;\n							for (k = 0; k < 1; k++)\n								u -= n[k] / n[k + 1];\n							left = u;\n')),
 ('f3', f('							uint32_t n[1];\n							int k;\n							n[0] = off & 0x1ffff;\n							left = 256;\n							for (k = 0; k < 1; k++)\n								left -= n[k] / 512;\n')),
 ('f4', f('							uint32_t n[1];\n							uint32_t u = 256;\n							int k;\n							n[0] = off & 0x1ffff;\n							for (k = 0; k < 1; k++)\n								u -= n[k] / 512;\n							left = u;\n')),
 ('f5', f('							uint32_t n[2];\n							uint32_t u = 0;\n							int k;\n							n[0] = 256;\n							n[1] = (off & 0x1ffff) / 512;\n							for (k = 0; k < 2; k++)\n								u = n[k] - u;\n							left = u;\n')),
 ('f6', f('							uint32_t n[2];\n							uint32_t u = 0;\n							int k;\n							n[0] = -256;\n							n[1] = (off & 0x1ffff) / 512;\n							for (k = 0; k < 2; k++)\n								u += n[k];\n							left = -u;\n')),
 ('f7', f('							uint32_t n[2];\n							uint32_t u = 256;\n							int k;\n							n[0] = (off & 0x1ffff) / 512;\n							n[1] = 0;\n							for (k = 0; k < 2; k++)\n								u -= n[k];\n							left = u;\n')),
]
AXES = [TY, FO]
