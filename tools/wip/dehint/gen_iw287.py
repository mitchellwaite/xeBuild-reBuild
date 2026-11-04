# attempt 23: which arm of the off & 0x1ffff test survives as the forwarder decides whether unswitch frees the original's PRE PHI after the copy's (inferred, see notes): forms of `left` with one arm or the arms' order swapped.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw287.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
LL = [
 ('', []),
 ('o1', [(L0, '						left = 256;\n						if (off & 0x1ffff)\n							left = 256 - (off & 0x1ffff) / 512;\n')]),
 ('o2', [(L0, '						left = 256;\n						if (off & 0x1ffff)\n							left -= (off & 0x1ffff) / 512;\n')]),
 ('o3', [(L0, '						left = !(off & 0x1ffff) ? 256 : 256 - (off & 0x1ffff) / 512;\n')]),
 ('o4', [(L0, '						if (!(off & 0x1ffff))\n							left = 256;\n						else\n							left = 256 - (off & 0x1ffff) / 512;\n')]),
 ('o5', [(L0, '						if (off & 0x1ffff)\n							goto partblk;\n						left = 256;\n						goto havepg;\npartblk:\n						left = 256 - (off & 0x1ffff) / 512;\nhavepg:\n')]),
 ('o6', [(L0, '						left = 256 - (off & 0x1ffff) / 512;\n')]),
 ('o7', [(L0, '						left = 256 - ((off & 0x1ffff) ? (off & 0x1ffff) / 512 : 0);\n')]),
 ('o8', [(L0, '						left = (off & 0x1ffff) ? (0x20000 - (off & 0x1ffff)) / 512 : 256;\n')]),
 ('o9', [(L0, '						left = 256;\n						if ((off & 0x1ffff) != 0)\n							left = (0x20000 - (off & 0x1ffff)) >> 9;\n')]),
 ('oa', [(L0, '						{ uint32_t ob = off & 0x1ffff;\n						left = 256;\n						if (ob)\n							left -= ob / 512;\n						}\n')]),
 ('ob', [(L0, '						left = 256;\n						if (off & 0x1ffff) {\n							left -= (off & 0x1ffff) / 512;\n						}\n')]),
]
AXES = [LL]
