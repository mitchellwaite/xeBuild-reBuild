"""checkBlock's pin_t: types of m and t (signed char: signed compare, sign extend known non-negative) on the switch forms and plain tests."""
FOCUS = ['_checkBlock']
src = open('src/image_read.c', newline='').read().replace('\r\n', '\n')
i = src.index('				uint8_t m = b[524] & 0x3f;')
j = src.index('			} else {\n				if (lba > 0 && block < numBlocks - 34 && lba != block)')
OLD = src[i:j]
k = OLD.index('log_printf(0, "\\n\\n****************  WARNING')
e = OLD.index('xb.nandMu = 1;') + len('xb.nandMu = 1;')
W = OLD[k:e] + '\n'
D = {
 'u8i': 'uint8_t m = b[524] & 0x3f; int t = m;\n',
 'c_i': 'char m = b[524] & 0x3f; int t = m;\n',
 'sci': 'signed char m = b[524] & 0x3f; int t = m;\n',
 's_i': 'short m = b[524] & 0x3f; int t = m;\n',
 'u16': 'unsigned short m = b[524] & 0x3f; int t = m;\n',
 'cc': 'char m = b[524] & 0x3f; char t = m;\n',
 'cs': 'char m = b[524] & 0x3f; short t = m;\n',
 'us': 'uint8_t m = b[524] & 0x3f; short t = m;\n',
 'ic': 'int m = b[524] & 0x3f; char t = m;\n',
 'iu': 'int m = b[524] & 0x3f; uint8_t t = m;\n',
 'ii': 'int m = b[524] & 0x3f; int t = m;\n',
 'cs0': 'char m = b[524]; int t = m & 0x3f;\n',
 'us0': 'uint8_t m = b[524]; int t = m & 0x3f;\n',
 'it': 'int t = b[524] & 0x3f; uint8_t m = t;\n',
 'itc': 'int t = b[524] & 0x3f; char m = t;\n',
}
F = {
 'and': f'if (t <= 0x29 && m) {{ {W} }}',
 'nest': f'if (t <= 0x29) {{ if (m) {{ {W} }} }}',
 'bs': f'if (t <= 0x29) {{ switch (m) {{ case 0: break; default: {W} }} }}',
 'bt': f'if (t <= 0x29) {{ switch (t) {{ case 0: break; default: {W} }} }}',
 'gt': f'if (t > 0x29) ; else if (m) {{ {W} }}',
 'ret': f'if (m > 0 && t < 0x2a) {{ {W} }}',
 'bm0': f'if (t <= 0x29) {{ if (m != 0) {{ {W} }} }}',
 'neg': f'if (!(t > 0x29) && !(m == 0)) {{ {W} }}',
}
AX = []
for kd, d in D.items():
    for kf, f in F.items():
        AX.append((kd + '.' + kf, [(OLD, d + f + '\n')]))
AXES = [AX]
