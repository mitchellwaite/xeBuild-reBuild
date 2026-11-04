# attempt 8: n6 (lnp2 AND pin_t gone; imgAdd and clones right): imgAddFile's compare and 0x30/0x34 slots with one local test (net -1 if everything else holds).
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n6.c')
FOCUS = ['_imgAddFile']
H0 = '	if (imgFits(off, len)) {\n		fsFiles[nFsFiles].block'
H1 = '		fsFiles[nFsFiles].time = *time;\n		if (!xb.bigBlock)\n'
H2 = '		if (!xb.bigBlock)\n			imgAdd(off, data, len, 0, 0xffff, 1);\n'
BODY = ['len++;', 'len += 0x4000;', 'off++;', 'off += 0x4000;', 'len = 0;', 'off = 0;']
COND = ['(len & 0x3fff) > 0x3fff', '(off & 0x3fff) > 0x3fff', '(off & 0xff) > 0xff']
A = [('', [])]
for ci, c in enumerate(COND):
    for bi, b in enumerate(BODY):
        d = '	if (%s)\n		%s\n' % (c, b)
        A.append(('h%d%d' % (ci, bi), [(H0, d + H0)]))
        d2 = '		if (%s)\n			%s\n' % (c, b)
        A.append(('m%d%d' % (ci, bi), [(H1, d2 + H1)]))
        A.append(('n%d%d' % (ci, bi), [(H2, d2 + H2)]))
AXES = [A]
