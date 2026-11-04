# attempt 23: a cast chain in the nonzero arm, `(int)` then back to unsigned: forwprop3/ccp3 strip such chains after dce3 (seen on left's own in the dumps), leaving a dead cheap cast in the arm that lim2 doesn't move and dce4 removes, so the arm outlives lim2's cleanup.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw290.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
def arm(body):
    return [(L0, '						if (off & 0x1ffff) {\n' + body + '						} else\n							left = 256;\n')]
LL = [
 ('', []),
 ('c4', [(L0, '						if (off & 0x1ffff)\n							left = 256 - (off & 0x1ffff) / 512;\n						else\n							left = 256;\n')]),
 ('i1', arm('							int o = off & 0x1ffff;\n							left = 256 - (uint32_t)o / 512;\n')),
 ('i2', arm('							int o = off & 0x1ffff;\n							left = 256 - o / 512;\n')),
 ('i3', arm('							int o = off & 0x1ffff;\n							uint32_t u = o;\n							left = 256 - u / 512;\n')),
 ('i4', arm('							int o = off & 0x1ffff;\n							left = 256 - (o >> 9);\n')),
 ('i5', arm('							int o = off & 0x1ffff;\n							left = 256 - ((uint32_t)o >> 9);\n')),
 ('i6', arm('							int o;\n							o = off & 0x1ffff;\n							o /= 512;\n							left = 256 - o;\n')),
 ('i7', arm('							int o;\n							o = off & 0x1ffff;\n							o >>= 9;\n							left = 256 - o;\n')),
 ('i8', arm('							short o = off & 0x1ffff;\n							left = 256 - (uint32_t)o / 512;\n')),
 ('i9', arm('							left = off & 0x1ffff;\n							left = 256 - (uint32_t)left / 512;\n')),
 ('ia', arm('							left = off & 0x1ffff;\n							left = 256 - left / 512;\n')),
 ('ib', arm('							left = off & 0x1ffff;\n							left /= 512;\n							left = 256 - left;\n')),
 ('ic', arm('							left = off & 0x1ffff;\n							left >>= 9;\n							left = 256 - left;\n')),
 ('id', arm('							left = (off & 0x1ffff) >> 9;\n							left = 256 - left;\n')),
 ('ie', arm('							left = (off & 0x1ffff) / 512;\n							left = 256 - left;\n')),
 ('if', [(L0, '						left = off & 0x1ffff;\n						if (left)\n							left = 256 - (uint32_t)left / 512;\n						else\n							left = 256;\n')]),
 ('ig', [(L0, '						left = off & 0x1ffff;\n						if (left)\n							left = 256 - left / 512;\n						else\n							left = 256;\n')]),
 ('ih', [(L0, '						left = off & 0x1ffff;\n						left = left ? 256 - left / 512 : 256;\n')]),
 ('ii', [(L0, '						left = off & 0x1ffff;\n						left = left ? 256 - (uint32_t)left / 512 : 256;\n')]),
 ('ij', [(L0, '						left = off & 0x1ffff;\n						left = left ? 256 - (left >> 9) : 256;\n')]),
]
AXES = [LL]
