# attempt 4: on c4a6 (10 lines: compare flips only): one dead test put back somewhere, any form, to fix imgAdd's `_1 != ivtmp` compare (still fewer tricks than 16)
import os
BASE = os.environ.get('IWB', 'build/iw/a4/c4a6.c')
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
FIT = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
LOC = {
 'mc': '	memcpy(xb.hdr + off, src, len);\n',
 'lp': '		if (x > first + 0x4000)\n			blocks += 2;\n',
 't': "		t = type - '1';\n",
 'nx': '	if (next != 0xf1f1) {\n',
 'fs': '			if (x > first + 0x4000)\n				blocks++;\n',
 'nf': '		if (next == 0xffff) {\n',
 'ie': '	imgEnd = off + len;\n	return 0;\n}\n\nint imgFits',
}
COND = {'g': 'x > first + 0x4000', 'l': 'x + 0x4000 < first', 'm': '(len & 0x3fff) > 0x3fff'}
BODY = {'bp': 'blocks++;', 'sp': 'start++;', 'b2': 'blocks += 2;'}
ax = [('', [])]
for ln, l in LOC.items():
    ind = '\t' * (len(l) - len(l.lstrip('\t')))
    for cn, c in COND.items():
        for bn, b in BODY.items():
            ax.append((f'{ln}{cn}{bn}', [(l, f'{ind}if ({c})\n{ind}\t{b}\n' + l)]))
AXES = [
 ax,
 [('', []), ('L1', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')])],
 [('', []), ('F1', [(FIT, '	if (__builtin_expect(lim >= end, 1)) {\n')])],
]
