"""checkBlock's pin_t: b[524] & 0x3f as a 6-bit bit-field (FsBlockType in the NAND metadata): VRP has no constant range on the load, so it doesn't narrow the compare."""
FOCUS = ['_checkBlock']
src = open('src/image_read.c', newline='').read().replace('\r\n', '\n')
i = src.index('				uint8_t m = b[524] & 0x3f;')
j = src.index('			} else {\n				if (lba > 0 && block < numBlocks - 34 && lba != block)')
OLD = src[i:j]
k = OLD.index('log_printf(0, "\\n\\n****************  WARNING')
e = OLD.index('xb.nandMu = 1;') + len('xb.nandMu = 1;')
W = OLD[k:e] + '\n'
S8 = 'struct { uint8_t type : 6; uint8_t ecc : 2; } *s = (void *)(b + 524);\n'
SU = 'struct { unsigned type : 6; unsigned ecc : 2; } __attribute__((packed)) *s = (void *)(b + 524);\n'
F = {
 'p_and': 'if (s->type <= 0x29 && s->type) {%s}',
 'p_nest': 'if (s->type <= 0x29) { if (s->type) {%s} }',
 'p_zf': 'if (s->type && s->type <= 0x29) {%s}',
 'p_sw': 'if (s->type <= 0x29) { switch (s->type) { case 0: break; default: %s} }',
 'tm_and': 'uint8_t m = s->type; if (m <= 0x29 && m) {%s}',
 'ti_and': 'int m = s->type; if (m <= 0x29 && m) {%s}',
 'ti_nest': 'int m = s->type; if (m <= 0x29) { if (m) {%s} }',
 'tm_nest': 'uint8_t m = s->type; if (m <= 0x29) { if (m) {%s} }',
 'ti2': 'uint8_t m = s->type; int t = m; if (t <= 0x29 && m) {%s}',
 'ti3': 'int t = s->type; if (t <= 0x29 && s->type) {%s}',
 'lt': 'if (s->type < 0x2a && s->type) {%s}',
 'neg': 'if (!(s->type >= 0x2a) && s->type != 0) {%s}',
 'ne0': 'if (s->type <= 0x29 && s->type != 0) {%s}',
}
AX = []
for kd, d in {'s8': S8, 'su': SU}.items():
    for kf, f in F.items():
        AX.append((kd + '.' + kf, [(OLD, d + (f % W) + '\n')]))
AXES = [AX]
