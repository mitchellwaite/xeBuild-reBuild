# attempt 23: a scope clobber as the statement that keeps the nonzero arm non-empty at lim2's cleanup: a local array or struct declared inside the arm. A clobber has no code. Probes of how long it lives, by iw23arm.py.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw293.py -n 30 -t 4`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
def arm(body):
    return [(L0, '						if (off & 0x1ffff) {\n' + body + '						} else\n							left = 256;\n')]
LL = [
 ('', []),
 ('c1', arm('							uint32_t n[1];\n							n[0] = (off & 0x1ffff) / 512;\n							left = 256 - n[0];\n')),
 ('c2', arm('							struct { uint32_t n; } v;\n							v.n = (off & 0x1ffff) / 512;\n							left = 256 - v.n;\n')),
 ('c3', arm('							uint32_t n[2];\n							int k;\n							n[0] = off & 0x1ffff;\n							n[1] = 512;\n							left = 256;\n							for (k = 0; k < 1; k++)\n								left -= n[k] / n[k + 1];\n')),
 ('c4', arm('							uint32_t n[2];\n							n[0] = off & 0x1ffff;\n							n[1] = n[0] / 512;\n							left = 256 - n[1];\n')),
 ('c5', arm('							uint32_t n[2];\n							int k;\n							n[0] = 256;\n							n[1] = (off & 0x1ffff) / 512;\n							left = 0;\n							for (k = 0; k < 2; k++)\n								left = n[k] - left;\n')),
 ('c6', arm('							struct { uint32_t a, b; } v = { off & 0x1ffff, 512 };\n							left = 256 - v.a / v.b;\n')),
 ('c7', arm('							uint32_t n;\n							uint32_t *q = &n;\n							*q = (off & 0x1ffff) / 512;\n							left = 256 - n;\n')),
]
AXES = [LL]
