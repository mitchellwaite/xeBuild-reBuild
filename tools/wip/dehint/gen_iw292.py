# attempt 23: the value computed before the off & 0x1ffff test, so the nonzero arm is empty at PRE: its true edge is critical, crited1's block for it has a high index and takes PRE's chain, the const arm's block has a lower index and goes first at lim2's cleanup.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw292.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
D0 = '	int left;\n'
LL = [
 ('', []),
 ('q1', [(L0, '						left = 256 - (off & 0x1ffff) / 512;\n						if (off & 0x1ffff) {\n						} else\n							left = 256;\n')]),
 ('q2', [(L0, '						left = 256 - (off & 0x1ffff) / 512;\n						left = (off & 0x1ffff) ? left : 256;\n')]),
 ('q3', [(L0, '						left = 256 - (off & 0x1ffff) / 512;\n						if (!(off & 0x1ffff))\n							left = 256;\n')]),
 ('q4', [(L0, '						{ int r = 256 - (off & 0x1ffff) / 512;\n						if (off & 0x1ffff)\n							left = r;\n						else\n							left = 256;\n						}\n')]),
 ('q5', [(L0, '						{ uint32_t r = 256 - (off & 0x1ffff) / 512;\n						if (off & 0x1ffff)\n							left = r;\n						else\n							left = 256;\n						}\n')]),
 ('q6', [(L0, '						{ uint32_t o = off & 0x1ffff, r = 256 - o / 512;\n						left = o ? r : 256;\n						}\n')]),
 ('q7', [(L0, '						{ uint32_t o = off & 0x1ffff, n = o / 512;\n						left = o ? 256 - n : 256;\n						}\n')]),
 ('q8', [(L0, '						{ uint32_t o = off & 0x1ffff, n = o / 512;\n						if (o)\n							n = 256 - n;\n						else\n							n = 256;\n						left = n;\n						}\n')]),
 ('q9', [(L0, '						{ uint32_t o = off & 0x1ffff, n = 256 - o / 512;\n						if (!o)\n							n = 256;\n						left = n;\n						}\n')]),
 ('qa', [(L0, '						{ uint32_t o = off & 0x1ffff, n = o / 512;\n						left = 256;\n						if (o)\n							left -= n;\n						}\n')]),
]
AXES = [LL]
