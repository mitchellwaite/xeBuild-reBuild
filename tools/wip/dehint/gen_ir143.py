"""checkBlock's pin_t: a switch is opaque to reassoc's range test: the zero test or the bound as a switch, no asm."""
FOCUS = ['_checkBlock']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('				uint8_t m = b[524] & 0x3f;')
j = src.index('			} else {\n				if (lba > 0 && block < numBlocks - 34 && lba != block)')
OLD = src[i:j]
k = OLD.index('log_printf(0, "\\n\\n****************  WARNING')
e = OLD.index('xb.nandMu = 1;') + len('xb.nandMu = 1;')
W = OLD[k:e] + '\n'
D = {'iu': 'uint8_t m = b[524] & 0x3f; int t = m;\n', 'uu': 'uint8_t m = b[524] & 0x3f; uint8_t t = m;\n', 'ii': 'int m = b[524] & 0x3f; int t = m;\n', 'tu': 'int t = b[524] & 0x3f; uint8_t m = t;\n'}
F = {
 'zs': f'switch (m) {{ case 0: break; default: if (t <= 0x29) {{ {W} }} }}',
 'bs': f'if (t <= 0x29) {{ switch (m) {{ case 0: break; default: {W} }} }}',
 'bs2': f'if (t <= 0x29) switch (m) {{ default: {W} case 0: break; }}',
 'bt': f'if (t <= 0x29) {{ switch (t) {{ case 0: break; default: {W} }} }}',
 'zt': f'switch (t) {{ case 0: break; default: if (m <= 0x29) {{ {W} }} }}',
 'zr': f'switch (t) {{ case 0: break; default: if (t < 0x2a) {{ {W} }} }}',
 'bg': f'if (t > 0x29) ; else switch (m) {{ case 0: break; default: {W} }}',
 'rg': f'switch (t) {{ case 1 ... 0x29: {W} break; }}',
 'rg2': f'switch (t) {{ case 0: case 0x2a ... 0x3f: break; default: {W} }}',
 'rg3': f'switch (m) {{ case 0: break; case 0x2a ... 0x3f: break; default: {W} }}',
 'rg4': f'switch (t) {{ case 0x2a ... 0x3f: case 0: break; default: {W} }}',
 'fl': f'if (t <= 0x29) {{ int z; switch (m) {{ case 0: z = 1; break; default: z = 0; }} if (!z) {{ {W} }} }}',
}
AX = []
for kd, d in D.items():
    for kf, f in F.items():
        AX.append((kd + '.' + kf, [(OLD, d + f + '\n')]))
AXES = [AX]
