# attempt 23: forms of a short table loop in the nonzero arm (all keep the arm through lim2 by the array's scope clobber), by left's and k's type and the s[9] statement. Scored by iw23sw.py.
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw295.py build/iw/a23/na.c 4 40`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
D = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n	int left;\n'
S9 = '						s[9] = (left - pages) >> 2;\n'
TY = [
 ('', []),
 ('lu', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, left;\n')]),
]
def f(body):
    return [(L0, '						if (off & 0x1ffff) {\n' + body + '						} else\n							left = 256;\n')]
I = '							'
ARRS = {
 'a': (I + 'uint32_t n[2];\n', I + 'n[0] = 256;\n' + I + 'n[1] = (off & 0x1ffff) / 512;\n'),
 'b': (I + 'uint32_t n[2] = { 256, (off & 0x1ffff) / 512 };\n', ''),
 'c': (I + 'int n[2];\n', I + 'n[0] = 256;\n' + I + 'n[1] = (off & 0x1ffff) / 512;\n'),
}
LOOPS = {
 'p': (I + 'int k;\n', I + 'left = n[0];\n' + I + 'for (k = 1; k < 2; k++)\n' + I + '	left -= n[k];\n'),
 'q': (I + 'uint32_t k;\n', I + 'left = n[0];\n' + I + 'for (k = 1; k < 2; k++)\n' + I + '	left -= n[k];\n'),
 'r': (I + 'int k;\n' + I + 'uint32_t u;\n', I + 'u = n[0];\n' + I + 'for (k = 1; k < 2; k++)\n' + I + '	u -= n[k];\n' + I + 'left = u;\n'),
 's': (I + 'int k;\n', I + 'left = 0;\n' + I + 'for (k = 1; k >= 0; k--)\n' + I + '	left = n[k] - left;\n'),
 't': (I + 'int k;\n', I + 'left = n[0];\n' + I + 'for (k = 1; k != 2; k++)\n' + I + '	left -= n[k];\n'),
 'u': (I + 'int k = 1;\n', I + 'left = n[0];\n' + I + 'while (k < 2)\n' + I + '	left -= n[k++];\n'),
}
FO = [('', [])]
for al, (ad, ai) in ARRS.items():
    for ll, (ld, lb) in LOOPS.items():
        FO.append((al + ll, f(ad + ld + ai + lb)))
SL = [
 ('', []),
 ('s4', [(S9, '						s[9] = (left - (int)pages) >> 2;\n')]),
 ('s5', [(S9, '						s[9] = (uint32_t)(left - (int)pages) >> 2;\n')]),
 ('s1', [(S9, '						left -= pages;\n						s[9] = left >> 2;\n')]),
]
AXES = [TY, FO, SL]
