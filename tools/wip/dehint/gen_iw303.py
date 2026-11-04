# attempt 24: gen_iw301 keeps imgAdd clean, but its else-only memset brings the call predictor to the off & 0x1ffff test (writeFsTable 340+). A call on both paths should cancel that. M* are mechanism probes, the first forms a person might write.
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw303.py build/iw/a24/nt.c 4 60`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
RO = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						left -= pages;\n						s[9] = left >> 2;\n'
OLD = L0 + RO + S9
I = '						'
M = '(off & 0x1ffff)'
def b(*l):
    return ''.join(I + x + '\n' for x in l)
R = ['	if (pages & 3)', '		pages = (pages + 4) & ~3;']
TAILS = {
 'j': R + ['	used[1] = pages;', '	left = 256 - used[0] - used[1];'],
 'l': ['	left = 256 - used[0];'] + R + ['	left -= pages;'],
}
Z = 'memset(used, 0, sizeof(used));'
HEADS = {
 'b1': ['	if ' + M + ' {', '		' + Z, '		used[0] = ' + M + ' / 512;', '	} else', '		' + Z],
 'b2': ['	if (!' + M + ')', '		' + Z, '	else {', '		' + Z, '		used[0] = ' + M + ' / 512;', '	}'],
 'c1': ['	if ' + M + ' {', '		' + Z, '		used[0] = ' + M + ' / 512;', '	} else', '		used[0] = 0;'],
 'd1': ['	if ' + M, '		memcpy(used, &(uint32_t[2]){ ' + M + ' / 512, 0 }, sizeof(used));', '	else', '		' + Z],
}
FO = [('', [])]
for h, hb in HEADS.items():
    for t, tb in TAILS.items():
        FO.append((h + t, [(OLD, b('{', '	uint32_t used[2];', '', *hb, *tb, '	s[9] = left >> 2;', '}'))]))
AXES = [FO]
