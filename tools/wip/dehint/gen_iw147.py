# attempt 8: n8: one dead test in imgAdd for constprop.1's compare (net 0 by itself: only worth it if writeFsTable then sheds its dead test or attribute).  Mostly to learn which position moves it.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
P = {
 'h': '	memcpy(xb.hdr + off, src, len);\n',
 'l': '		blk = start + b;\n',
 'm': '		p = 0;\n',
 'n': '			memset(s, 0, 16);\n',
 'e': '	if (next != 0xf1f1) {\n',
 'x': '	imgEnd = off + len;\n	return 0;\n}\n\n/* an `if`',
}
COND = ['(len & 0x3fff) > 0x3fff', 'x > first + 0x4000', 'x + 0x4000 < first', '(tail & 0x3fff) > 0x3fff']
BODY = ['blocks++;', 'blocks += 2;', 'start++;', 'len++;']
A = [('', [])]
for pk, pv in P.items():
    for ci, c in enumerate(COND):
        for bi, b in enumerate(BODY):
            ind = '	' if pk in 'hex' else ('		' if pk in 'lm' else '			')
            A.append(('%s%d%d' % (pk, ci, bi), [(pv, ind + 'if (%s)\n' % c + ind + '	%s\n' % b + pv)]))
AXES = [A]
