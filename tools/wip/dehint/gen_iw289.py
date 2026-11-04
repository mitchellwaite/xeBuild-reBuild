# attempt 23: mechanism probes, not candidates: something in the nonzero arm that lim2 can't move, to see whether the arm surviving lim2's cleanup gives the target order.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw289.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
LL = [
 ('', []),
 ('asm', [(L0, '						if (off & 0x1ffff) {\n							__asm__("");\n							left = 256 - (off & 0x1ffff) / 512;\n						} else\n							left = 256;\n')]),
 ('asm2', [(L0, '						if (off & 0x1ffff) {\n							left = 256 - (off & 0x1ffff) / 512;\n							__asm__("");\n						} else\n							left = 256;\n')]),
]
AXES = [LL]
